# MIT License

# Copyright (c) 2022 Loschmidt Laboratories & IT4Innovations

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import hashlib
import json
import logging
import os
import subprocess

import pandas as pd
import pylru
import shutil

from dataclasses import dataclass
from enum import Enum, auto
from io import StringIO
from typing import List, Optional

from . import CaverDock, CaverDockTrajectory, DiscretizedTunnel, Direction, EnergyProfileAnalysis, Ligand, MGLToolsWrapper, Receptor, TrajectoryType, discretize_tunnel, load_tunnel
from .utils import check_path_exists, get_basename, log


@dataclass
class InputFile:
    path: str


class Stream(Enum):
    STDOUT = auto()
    STDERR = auto()


class Workdir:

    def __init__(self, directory: str, memory_cache_size=1000):
        self.directory = os.path.abspath(directory)
        self.cache_directory = os.path.join(self.directory, "cache")
        os.makedirs(self.cache_directory, exist_ok=True)
        self.log_directory = os.path.join(self.directory, "logs")
        os.makedirs(self.log_directory, exist_ok=True)
        self.cache = pylru.lrucache(memory_cache_size)

    def resolve_entry(self, load_fn, compute_fn, args):
        key = self.create_key(args)
        entry_path = self.entry_path(key)
        if self.has_entry(key):
            resolved = self.cache.get(key)
            if resolved is not None:
                return resolved
            return load_fn(entry_path)
        value = compute_fn(entry_path)
        self.cache[key] = value
        return value

    def entry_path(self, key: str) -> str:
        return os.path.join(self.cache_directory, key)

    def has_entry(self, key: str) -> bool:
        return os.path.isfile(self.entry_path(key)) or key in self.cache

    def create_key(self, args: dict) -> str:
        args = dict(args)
        for (key, value) in args.items():
            if isinstance(value, InputFile):
                check_path_exists(value.path, f"File {value.path} not found")
                args[key] = hash_file(value.path)

        hash = hashlib.md5()
        hash.update(json.dumps(args, indent=False).encode())
        return hash.hexdigest()

    def log_file(self, step: str, path: str, stream: Optional[Stream], include_path_hash: bool = True,
                 extract_basename: bool = True):
        if extract_basename:
            try:
                name = os.path.splitext(os.path.basename(path))[0]
            except:
                name = path
        else:
            name = path

        log_name = f"{step}_{name}"
        if include_path_hash:
            hash = hashlib.md5()
            hash.update(path.encode())
            log_name += f"_{hash.hexdigest()}"
        log_name += f".{stream.name.lower() if stream else 'log'}"

        return os.path.join(self.log_directory, log_name)


def create_args_cache_value(args: Optional[List[str]]) -> str:
    if args is None:
        return ""
    return " ".join(str(v) for v in args)


def check_args(args: Optional[List[str]]):
    if args is not None:
        for argument in args:
            if not isinstance(argument, str):
                raise Exception(f"Each argument must be a string. "
                                f"Argument `{argument}` has type `{type(argument)}`.")


class Experiment:
    """
    Utility class for running experiments.

    It takes care of storing input/output data of experiments and caching them so that they are
    not recomputed needlessly. The caching is based on hashes of experiment input files.

    :param workdir: Working directory
    :param name: Name of the experiment
    :param mgltools: MGLTools package wrapper
    :param caverdock: CaverDock executable wrapper
    """

    def __init__(self, workdir: Workdir, name: str, mgltools: MGLToolsWrapper, caverdock: CaverDock):
        self.workdir = workdir
        self.name = name
        self.mgltools = mgltools
        self.caverdock = caverdock

        self.directory = os.path.join(workdir.directory, "experiments", self.name)
        os.makedirs(self.directory, exist_ok=True)
        self.input_dir = os.path.join(self.directory, "inputs")
        os.makedirs(self.input_dir, exist_ok=True)
        self.intermediate_dir = os.path.join(self.directory, "intermediate")
        os.makedirs(self.intermediate_dir, exist_ok=True)
        self.result_dir = os.path.join(self.directory, "results")
        os.makedirs(self.result_dir, exist_ok=True)
        self.caverdock_directory = os.path.join(self.intermediate_dir, "caverdock")
        os.makedirs(self.caverdock_directory, exist_ok=True)

    def store_input_file(self, file: str, overwrite=True):
        """
        Copies the passed input `file` to the experiment directory.
        """
        basename = os.path.basename(file)
        path = os.path.join(self.input_dir, basename)
        if not overwrite and os.path.isfile(path):
            logging.warning(
                f"Input with name {basename} for experiment {self.name} already exists")
        shutil.copyfile(file, path)

    def intermediate_path(self, file: str):
        """
        Get the path of an intermediate result with the given filename.
        """
        return os.path.join(self.intermediate_dir, file)

    def result_path(self, file: str):
        """
        Get the path of a result with the given filename.
        """
        return os.path.join(self.result_dir, file)

    def prepare_ligand(self, ligand_path: str, args: List[str] = None) -> Ligand:
        """
        Prepare a ligand using MGLTools.
        The result is cached if the workdir and the input ligand file stays the same.

        :param ligand_path: Path to a ligand file
        :param args: Additional arguments passed to MGLToolsWrapper::prepare_ligand
        """
        check_args(args)
        cache_key = dict(
            ligand=InputFile(ligand_path),
            args=create_args_cache_value(args)
        )

        def compute(output_path: str):
            log.info(f"Preparing ligand {ligand_path}")
            with open(self.workdir.log_file("prepare_ligand", ligand_path, None), "w") as log_fh:
                return self.mgltools.prepare_ligand(
                    ligand_path, output_path,
                    stdout=log_fh,
                    stderr=subprocess.STDOUT,
                    args=args
                )

        def load(input_path: str):
            log.debug(f"Ligand {ligand_path} already prepared. Loading from cache...")
            return Ligand(input_path)

        return self.workdir.resolve_entry(load, compute, cache_key)

    def prepare_receptor(self, receptor_path: str, args: List[str] = None) -> Receptor:
        """
        Prepare a receptor using MGLTools.
        The result is cached if the workdir and the input receptor file stays the same.

        :param receptor_path: Path to a receptor file
        :param args: Additional arguments passed to MGLToolsWrapper::prepare_receptor
        """
        check_args(args)
        cache_key = dict(
            receptor=InputFile(receptor_path),
            args=create_args_cache_value(args)
        )

        def compute(output_path: str):
            log.info(f"Preparing receptor {receptor_path}")
            with open(self.workdir.log_file("prepare_receptor", receptor_path, None), "w") as log_fh:
                return self.mgltools.prepare_receptor(
                    receptor_path, output_path,
                    stdout=log_fh,
                    stderr=subprocess.STDOUT,
                    args=args
                )

        def load(input_path: str):
            log.debug(f"Receptor {receptor_path} already prepared. Loading from cache...")
            return Receptor(input_path)

        return self.workdir.resolve_entry(load, compute, cache_key)

    def discretize_tunnel(self, tunnel_path: str, delta: float, threads: Optional[int] = None) -> DiscretizedTunnel:
        """
        Discretize a tunnel.
        The result is cached if the workdir and the input tunnel file stays the same.
        """
        cache_key = dict(
            tunnel=InputFile(tunnel_path),
            delta=delta
        )

        def compute(output_path: str):
            log.info(f"Discretizing tunnel {tunnel_path}")
            tunnel = discretize_tunnel(
                load_tunnel(tunnel_path),
                delta=delta,
                threads=threads,
                log=self.workdir.log_file("discretizer", tunnel_path, None),
            )
            tunnel.write_to_file(output_path)
            return tunnel

        def load(input_path: str):
            log.debug(f"Tunnel {tunnel_path} already discretized. Loading from cache...")
            return DiscretizedTunnel.load_from_file(input_path)

        tunnel = self.workdir.resolve_entry(load, compute, cache_key)
        name = f"{get_basename(tunnel_path)}-discretized.dsd"
        tunnel.write_to_file(self.intermediate_path(name))
        return tunnel

    def run_caverdock(self,
                      ligand: Ligand,
                      receptor: Receptor,
                      tunnel: DiscretizedTunnel,
                      direction: Direction = Direction.OUT,
                      trajectory_type: TrajectoryType = TrajectoryType.LOWERBOUND,
                      mpi_processes: Optional[int] = None,
                      seed: Optional[int] = None,
                      catomnum: Optional[int] = None,
                      exhaustiveness: Optional[int] = None,
                      args: List[str] = None) -> CaverDockTrajectory:
        """
        Runs CaverDock trajectory computation.
        The result is cached if the workdir and the inputs (ligand, receptor, tunnel) stay the
        same.

        Returns a dictionary with "lb" (and "ub", if `upperbound` is True) keys that map to
        filenames containing the computed results.

        :param directory: The results and CaverDock configuration will be stored into this directory.
        :param ligand: Path to the input ligand.
        :param receptor: Path to the input receptor.
        :param tunnel: Discretized tunnel to be used for the computation.
        :param direction: Direction of the simulation IN or OUT.
        :param trajectory_type: Type of calculated simulation LOWERBOUND - only lowerbound, UPPERBOUND - both lowerbound and upperbound calculation.
        :param mpi_processes: Set the number of used MPI processes. If set to `None`, MPI will not be used.
        :param seed: Seed for random number generator.
        :param catomnum: Atom number from ligand pdbqt file which will be used as drag atom.
        :param exhaustiveness: Exhaustiveness setting for the docking algorithm.
        :param args: Additional arguments for CaverDock.
        """
        name = "caverdock"
        check_args(args)
        cache_key = dict(
            ligand=InputFile(ligand.path),
            receptor=InputFile(receptor.path),
            tunnel=hash_discretized_tunnel(tunnel),
            direction=direction.name,
            trajectory_type=trajectory_type.name,
            seed=seed,
            catomnum=catomnum,
            exhaustiveness=exhaustiveness,
            args=create_args_cache_value(args)
        )

        def compute(output_path: str):
            log.info(f"Running CaverDock calculation")
            with open(self.workdir.log_file("caverdock", self.name, None, False, False), "w") as log_fh:
                data = self.caverdock.run(self.caverdock_directory,
                                          name,
                                          ligand.path,
                                          receptor.path,
                                          tunnel,
                                          direction=direction,
                                          trajectory_type=trajectory_type,
                                          mpi_processes=mpi_processes,
                                          seed=seed,
                                          catomnum=catomnum,
                                          exhaustiveness=exhaustiveness,
                                          stdout=log_fh,
                                          stderr=subprocess.STDOUT,
                                          args=args)

            files = {
                "lb": data.lb,
                "ub": data.ub
            }
            compress_files(files, output_path)

            return data

        def load(input_path: str):
            log.debug(f"CaverDock calculation already finished. Loading from cache...")
            unpack_path = os.path.join(self.caverdock_directory, "unpacked")
            os.makedirs(unpack_path, exist_ok=True)
            files = decompress_files(input_path, unpack_path)
            return CaverDockTrajectory(tunnel, direction, files["lb"], files["ub"])

        return self.workdir.resolve_entry(load, compute, cache_key)


def compress_files(file_map, output_path: str):
    data = {}
    for (tag, file_path) in file_map.items():
        if file_path and os.path.isfile(file_path):
            with open(file_path) as f:
                data[tag] = f.read()  # TODO: store compressed and in binary form
        else:
            data[tag] = None
    with open(output_path, "w") as f:
        json.dump(data, f)


def decompress_files(input_path: str, unpack_dir: str) -> dict:
    data = {}
    with open(input_path) as f:
        stored = json.load(f)
        for (key, value) in stored.items():
            if value is not None:
                path = os.path.join(unpack_dir, key)
                with open(path, "w") as f:
                    f.write(value)
                data[key] = path
            else:
                data[key] = None
    return data


def hash_file(path: str) -> str:
    hash = hashlib.md5()

    with open(path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()


def hash_discretized_tunnel(tunnel: DiscretizedTunnel) -> str:
    state = hashlib.md5()

    io = StringIO()
    tunnel.write(io)

    io.seek(0)
    state.update(io.read().encode())
    return state.hexdigest()


def convert_eprofile_analysis(experiment_name: str, eprofile_analysis: EnergyProfileAnalysis, receptor_path: str, tunnel_path: str, ligand_path: str) -> pd.DataFrame:
    """
    Saves information from calculation into pandas Dataframe.

    :param experiment_name: Name of the simulation.
    :param eprofile_analysis: Object with calculated energy values from eprofile analysis.
    :param receptor_path: Path to the input receptro file.
    :param tunnel_path: Path to the input tunnel file.
    :param ligand_path: Path to the input ligand file.
    """
    return pd.DataFrame({
        "experiment": [experiment_name],
        "direction": [eprofile_analysis.direction.name],
        "trajectory_type": [eprofile_analysis.trajectory_type.name],
        "E_bound": [eprofile_analysis.E_bound],
        "E_max": [eprofile_analysis.E_max],
        "E_surface": [eprofile_analysis.E_surface],
        "k_on": [eprofile_analysis.k_on],
        "k_off": [eprofile_analysis.k_off],
        "dE_bs": [eprofile_analysis.dE_bs],
        "receptor": [receptor_path],
        "tunnel": [tunnel_path],
        "ligand": [ligand_path]
    })
