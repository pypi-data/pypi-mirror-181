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

import math
import os
import shutil
import subprocess

from dataclasses import dataclass
from typing import List, Optional, Tuple

from . import DiscretizedTunnel, Direction, EnergyProfile, TrajectoryType, create_energy_profile
from .tunnel import Vec3D
from .utils import check_path_exists, log


DEFAULT_CATOMNUM: int = 0
DEFAULT_EXHAUSTIVENESS: int = 1


@dataclass
class CaverDockTrajectory:
    """
    Creates energy profile from CaverDock calculation.
    """
    tunnel: DiscretizedTunnel
    direction: Direction
    lb: str
    ub: Optional[str] = None

    @property
    def energy_profile(self) -> EnergyProfile:
        return create_energy_profile(self.tunnel, self.ub if self.ub else self.lb, self.direction)

    @property
    def energy_profile_lowerbound(self) -> EnergyProfile:
        return create_energy_profile(self.tunnel, self.lb, self.direction)

    @property
    def energy_profile_upperbound(self) -> EnergyProfile:
        if not self.ub:
            return None
        return create_energy_profile(self.tunnel, self.ub, self.direction)


class CaverDockNotFoundError(Exception):
    pass


class CaverDock:
    """
    Wraps CaverDock and exposes a method to calculate lower/upper bounds.
    """
    def __init__(self, binary: Optional[str] = None):
        self.binary = os.path.abspath(binary) if binary else shutil.which("caverdock")
        if not self.binary:
            raise CaverDockNotFoundError("Cannot autodetect CaverDock binary path from the environment")
        check_path_exists(self.binary, "Expected CaverDock binary at", CaverDockNotFoundError)
        log.debug(f"CaverDock binary: {self.binary}")

    def run(self,
            directory: str,
            name: str,
            ligand: str,
            receptor: str,
            tunnel: DiscretizedTunnel,
            direction: Direction = Direction.OUT,
            trajectory_type: TrajectoryType = TrajectoryType.LOWERBOUND,
            mpi_processes: Optional[int] = None,
            seed: Optional[int] = None,
            catomnum: Optional[int] = None,
            exhaustiveness: Optional[int] = None,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            args: Optional[List[str]] = None) -> CaverDockTrajectory:
        """
        Runs CaverDock with the given `ligand`, `receptor` and `tunnel`.

        :param directory: The results and CaverDock configuration will be stored into this directory.
        :param name: Name of the computation (will be used for naming the result files).
        :param ligand: Path to the input ligand.
        :param receptor: Path to the input receptor.
        :param tunnel: Discretized tunnel to be used for the computation.
        :param direction: Direction of the simulation IN or OUT.
        :param trajectory_type: Type of calculated simulation LOWERBOUND - only lowerbound, UPPERBOUND - both lowerbound and upperbound calculation.
        :param mpi_processes: Set the number of used MPI processes. If set to `None`, MPI will not be used.
        :param seed: Seed for random number generator.
        :param catomnum: Atom number from ligand pdbqt file which will be used as drag atom.
        :param exhaustiveness: Exhaustiveness setting for the docking algorithm.
        :param stdout: Defines what happens with the STDOUT strings, see subprocess documentation.
        :param stderr: Defines what happens with the STDERR strings, see subprocess documentation.
        :param args: Additional arguments for CaverDock.
        """
        os.makedirs(directory, exist_ok=True)

        config_path = os.path.join(directory, f"caverdock.config")
        tunnel_path = os.path.join(directory, f"tunnel.dsd")

        ftunnel = tunnel if direction == Direction.OUT else tunnel.reverse()

        ftunnel.write_to_file(tunnel_path)
        with open(config_path, "w") as config_file:
            config = generate_caverdock_config(ligand, receptor, tunnel_path, seed=seed,
                                               catomnum=catomnum, exhaustiveness=exhaustiveness)
            config_file.write(config)

        # When running with tunnels, it must be executed with at least 2 MPI processes
        mpi_processes = mpi_processes or 2

        if seed is not None and mpi_processes > 2:
            log.warn("IMPORTANT: Seed does not guarantee deterministic results when more than 2 MPI proccesses are used!")

        self._run(directory, name, config_path, trajectory_type, mpi_processes, stdout, stderr, args)

        return CaverDockTrajectory(
            tunnel,
            direction,
            CaverDock._trajectory_path(directory, name, TrajectoryType.LOWERBOUND, trajectory_type),
            CaverDock._trajectory_path(directory, name, TrajectoryType.UPPERBOUND, trajectory_type)
        )

    def run_with_config(self,
                        directory: str,
                        name: str,
                        config_path: str,
                        trajectory_type: Optional[TrajectoryType] = None,
                        mpi_processes: Optional[int] = None,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        args: Optional[List[str]] = None) -> Tuple[str, str]:
        """
        Runs CaverDock with the custom configuration file.

        :param directory: The results and CaverDock configuration will be stored into this directory.
        :param name: Name of the computation (will be used for naming the result files).
        :param config_path: Path to the custom configuration file.
        :param trajectory_type: Type of calculated simulation LOWERBOUND - only lowerbound, UPPERBOUND - both lowerbound and upperbound calculation.
        :param mpi_processes: Set the number of used MPI processes. If set to `None`, MPI will not be used.
        :param stdout: Defines what happens with the STDOUT strings, see subprocess documentation.
        :param stderr: Defines what happens with the STDERR strings, see subprocess documentation.
        :param args: Additional arguments for CaverDock.
        """
        self._run(directory, name, config_path, trajectory_type, mpi_processes, stdout, stderr, args)
        return (
            CaverDock._trajectory_path(directory, name, TrajectoryType.LOWERBOUND, trajectory_type),
            CaverDock._trajectory_path(directory, name, TrajectoryType.UPPERBOUND, trajectory_type)
        )

    def _run(self,
             directory: str,
             name: str,
             config_path: str,
             trajectory_type: Optional[TrajectoryType],
             mpi_processes: Optional[int],
             stdout,
             stderr,
             args: Optional[List[str]]) -> None:
        command = [
            self.binary,
            "--config", os.path.abspath(config_path),
            "--out", name,
            "--log", "caverdock.log"
        ]

        if trajectory_type == TrajectoryType.LOWERBOUND:
            command += ["--final_state", "LB"]
        if args:
            command.extend(args)
        if mpi_processes:
            command = ["mpirun", "-np", str(mpi_processes)] + command

        log.info(f"Executing CaverDock command: {command}")
        subprocess.run(command, cwd=directory, check=True, stdout=stdout, stderr=stderr)

    @staticmethod
    def _trajectory_path(directory: str, name: str, trajectory_type: TrajectoryType, final_trajectory_type: Optional[TrajectoryType]):
        f = os.path.join(directory, get_result_path(name, trajectory_type))

        if trajectory_type == TrajectoryType.UPPERBOUND:
            if final_trajectory_type is None:
                return f if os.path.exists(f) else None

            if final_trajectory_type is not None and final_trajectory_type != TrajectoryType.UPPERBOUND:
                return None

        return f


def get_result_path(name: str, trajectory_type: TrajectoryType) -> str:
    end = "ub" if trajectory_type == TrajectoryType.UPPERBOUND else "lb"
    return f"{name}-{end}.pdbqt"


def calculate_dist_max(atoms: List[Vec3D]) -> float:
    dist_max = 0.0
    for i in range(0, len(atoms)):
        for j in range(i + 1, len(atoms)):
            dist = math.sqrt(
                pow(atoms[i][0] - atoms[j][0], 2.0) + pow(atoms[i][1] - atoms[j][1], 2.0) + pow(
                    atoms[i][2] - atoms[j][2], 2.0))
            if dist > dist_max:
                dist_max = dist
    dist_max *= 1.3  # approx of deformation
    dist_max += 3.0  # approx of max atom diameter
    return dist_max


def get_ligand_atoms(ligand_path: str) -> List[Vec3D]:
    atoms = []
    with open(ligand_path) as f:
        for line in f:
            words = line.strip().split()
            if words[0] == "ATOM":
                atoms.append(Vec3D(float(words[5]), float(words[6]), float(words[7])))
    return atoms


def calculate_tunnel_gridbox(ligand_path: str, tunnel: DiscretizedTunnel) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    atoms = get_ligand_atoms(ligand_path)
    dist_max = calculate_dist_max(atoms)

    # Set starting grid
    disk = tunnel.disks[0]
    box = [
        [disk.center[i] - disk.radius - dist_max for i in range(0, 3)],
        [disk.center[i] - disk.radius + dist_max for i in range(0, 3)]
    ]

    # Compute grid size according to tunnel
    for disk in tunnel.disks:
        for i in range(0, 3):
            if box[0][i] > disk.center[i] - disk.radius - dist_max:
                box[0][i] = disk.center[i] - disk.radius - dist_max
            if box[1][i] < disk.center[i] + disk.radius + dist_max:
                box[1][i] = disk.center[i] + disk.radius + dist_max

    center = [0, 0, 0]
    size = [0, 0, 0]
    for i in range(0, 3):
        size[i] = box[1][i] - box[0][i]
        center[i] = box[0][i] + size[i] / 2.0

    return tuple(center), tuple(size)


def generate_caverdock_config(
        ligand_path: str,
        receptor_path: str,
        tunnel_path: str,
        seed: Optional[int] = None,
        catomnum: Optional[int] = None,
        exhaustiveness: Optional[int] = None,
        additional_params: Optional[List[Tuple[str, str]]] = None
) -> str:
    """
    Creates custom configuration file.

    :param directory: The results and CaverDock configuration will be stored into this directory.
    :param name: Name of the computation (will be used for naming the result files).
    :param ligand_path: Path to the input ligand.
    :param receptor_path: Path to the input receptor.
    :param tunnel_path: Path to the discretized tunnel file.
    :param seed: Seed for random number generator.
    :param catomnum: Atom number from ligand pdbqt file which will be used as drag atom.
    :param exhaustiveness: Exhaustiveness setting for the docking algorithm.
    :param args: Additional parameters to write into the configuration file.
    """
    center, size = calculate_tunnel_gridbox(ligand_path, DiscretizedTunnel.load_from_file(tunnel_path))

    config = [
        ("receptor", os.path.abspath(receptor_path)),
        ("ligand", os.path.abspath(ligand_path)),
        ("tunnel", os.path.abspath(tunnel_path)),
        ("center_x", center[0]),
        ("center_y", center[1]),
        ("center_z", center[2]),
        ("size_x", int(size[0] + 0.5)),
        ("size_y", int(size[1] + 0.5)),
        ("size_z", int(size[2] + 0.5)),
        ("catomnum", catomnum if catomnum is not None else DEFAULT_CATOMNUM),
        ("exhaustiveness", exhaustiveness if exhaustiveness is not None else DEFAULT_EXHAUSTIVENESS),
        ("cpu", 1)
    ]

    if seed is not None:
        config.append(("seed", seed))

    if additional_params is not None:
        config += additional_params

    return "\n".join(map(lambda x: f"{x[0]} = {x[1]}", config)).strip()
