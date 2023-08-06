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

import click
import os

from typing import Optional
from zipfile import ZipFile

from .. import CaverDock, Direction, DiscretizedTunnel, MGLToolsWrapper, TrajectoryType, discretize_tunnel, load_tunnel
from ..utils import CLICK_CONTEXT_SETTINGS, init_logging, log


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option("-r", "--receptor", help="Path to receptor. If receptor file suffix is .pdbqt, preparation is skipped.",
              type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("-t", "--tunnel", help="Path to tunnel. If tunnel file suffix is .dsd, discretization is skipped. "
                                     "To skip extension, please use --skip-tunnel-extension flag.",
              type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("-l", "--ligand", help="Path to ligand. If ligand file suffix is .pdbqt, preparation is skipped.",
              type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("-d", "--direction", help="Direction",
              type=click.Choice([d.name for d in Direction], case_sensitive=False), required=False,
              default=Direction.OUT.name)
@click.option("-s", "--trajectory-type", help="Trajectory type",
              type=click.Choice([d.name for d in TrajectoryType], case_sensitive=False), required=False,
              default=TrajectoryType.LOWERBOUND.name)
@click.option("-n", "--name", help="Output file name template",
              type=click.STRING, required=False, default="analysis")
@click.option("-w", "--workdir", help="Workdir (default: current directory)",
              type=click.Path(exists=True, dir_okay=True, file_okay=False, writable=True), required=False)
@click.option("-o", "--output-archive", help="Path to output zip archive",
              type=click.Path(writable=True), required=False)
@click.option("-p", "--threads", help="Number of threads to use for calculation",
              type=click.IntRange(min=2), required=False)
@click.option("-c", "--caverdock", help="Path to CaverDock binary",
              type=click.Path(exists=True, dir_okay=False), required=False)
@click.option("-m", "--mgltools", "mgltools_path", help="Path to MGLTools root",
              type=click.Path(exists=True, file_okay=False), required=False)
@click.option("--keep-ligand-charges", help="Keep ligand charges",
              is_flag=True)
@click.option("--discretization-delta", help="Discretization delta",
              type=click.FloatRange(min_open=0), required=False, default=.3)
@click.option("--skip-tunnel-extension", help="Skip tunnel extension",
              is_flag=True)
@click.option("--tunnel-extension", help="Tunnel extension length in Angstroms",
              type=click.FloatRange(min_open=0), required=False, default=2)
@click.option("--tunnel-extension-step", help="Tunnel extension step in Angstroms",
              type=click.FloatRange(min_open=0), required=False, default=.2)
@click.option("-a", "--drag-atom", help="Ligand drag atom",
              type=click.IntRange(min=0), required=False)
@click.option("--seed", help="Seed",
              type=click.INT, required=False)
@click.option("--exhaustiveness", help="Exhaustiveness",
              type=click.IntRange(min=1), required=False)
@click.option("--delete-bottlenecks", help="Delete bottlenecks files",
              is_flag=True)
@click.option("--rename", help="Rename all files to same scheme",
              is_flag=True)
@click.option("-v", "--verbose", help="Increase log verbosity",
              is_flag=True)
def cmd(
        name: str, receptor: str, tunnel: str, ligand: str, direction: str, trajectory_type: str,
        workdir: Optional[str], output_archive: Optional[str], threads: Optional[int], mgltools_path: Optional[str],
        caverdock: Optional[str],
        discretization_delta: float, tunnel_extension: float, tunnel_extension_step: float,
        drag_atom: Optional[int], keep_ligand_charges: bool,
        skip_tunnel_extension: bool, delete_bottlenecks: bool, seed: Optional[int], exhaustiveness: Optional[int], verbose: bool,
        rename: bool
):
    init_logging(verbose)
    mgltools = MGLToolsWrapper(mgltools_path)
    caverdock = CaverDock(caverdock)

    tunnel = os.path.abspath(tunnel)
    receptor = os.path.abspath(receptor)
    ligand = os.path.abspath(ligand)
    output_archive = os.path.abspath(output_archive) if output_archive else None

    workdir = workdir or os.getcwd()
    os.chdir(workdir)
    workdir = os.getcwd()

    prepared_receptor = _get_file(receptor, "receptor", "pdbqt", rename)
    if receptor.lower().endswith(".pdbqt"):
        log.info("Receptor is already prepared. Skipping...")
        prepared_receptor = receptor
    else:
        log.info("Preparing receptor")
        with open("prepare_receptor.stdout", "w") as fh_stdout, open("prepare_receptor.stderr", "w") as fh_stderr:
            mgltools.prepare_receptor(receptor, prepared_receptor, stdout=fh_stdout, stderr=fh_stderr)
        log.info(f"Receptor successfuly prepared to file: {prepared_receptor}")

    prepared_ligand = _get_file(ligand, "ligand", "pdbqt", rename)
    if ligand.lower().endswith(".pdbqt"):
        log.info("Ligand is already prepared. Skipping...")
        prepared_ligand = ligand
    else:
        log.info("Preparing ligand")
        with open("prepare_ligand.stdout", "w") as fh_stdout, open("prepare_ligand.stderr", "w") as fh_stderr:
            mgltools.prepare_ligand(ligand, prepared_ligand, stdout=fh_stdout, stderr=fh_stderr,
                                    args=["-C"] if keep_ligand_charges else None)
        log.info(f"Ligand successfuly prepared to file: {prepared_ligand}")

    if tunnel.lower().endswith(".dsd"):
        log.info("Tunnel is already discretized. Skipping...")
        discretized_tunnel = DiscretizedTunnel.load_from_file(tunnel)
    else:
        log.info("Discretizing tunnel")
        discretized_tunnel = discretize_tunnel(load_tunnel(tunnel), delta=discretization_delta, threads=threads,
                                               log="discretizer.log")
        log.info("Tunnel successfuly discretized")

    if not skip_tunnel_extension:
        log.info("Extending tunnel")
        discretized_tunnel = discretized_tunnel.extend(tunnel_extension, tunnel_extension_step)

    log.info("Running CaverDock")
    trajectory = caverdock.run(
        workdir, name, prepared_ligand, prepared_receptor, discretized_tunnel, Direction[direction], TrajectoryType[trajectory_type],
        mpi_processes=threads, seed=seed, catomnum=drag_atom, exhaustiveness=exhaustiveness
    )

    if delete_bottlenecks:
        files = [f for f in os.listdir(workdir) if f.startswith("bottlenecks.dat.")]
        for f in files:
            os.remove(f)

    log.info("Storing lowerbound profile")
    trajectory.energy_profile_lowerbound.write_to_dat(f"{name}-lb.dat")

    if TrajectoryType[trajectory_type] == TrajectoryType.UPPERBOUND:
        log.info("Storing upperbound profile")
        trajectory.energy_profile_upperbound.write_to_dat(f"{name}-ub.dat")

    _compressdir(workdir, output_archive)


def _compressdir(dir: str, archive: Optional[str]):
    if archive is None:
        return

    if os.path.isfile(archive):
        os.remove(archive)

    files = os.listdir(dir)
    with ZipFile(archive, 'w') as myzip:
        for f in files:
            myzip.write(f)


def _get_file(orig_path: str, uni_name: str, ext: str, rename: bool) -> str:
    return os.path.abspath(
        f"{uni_name}.{ext}" if rename else f"{os.path.splitext(os.path.basename(orig_path))[0]}.{ext}"
    )


def main():
    cmd()
