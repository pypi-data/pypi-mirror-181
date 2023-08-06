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
import logging
import pandas as pd
import os
import sys

from dataclasses import dataclass, field
from tqdm import tqdm
from typing import Optional

from . import ActiveSiteLocation, BoundaryType, CaverDock, CaverDockNotFoundError, cfggen, Direction, DiscRanges, EnergyProfilePlot, Ligand, MGLToolsNotFoundError, MGLToolsWrapper, Receptor, TrajectoryType, plot_results
from .experiment import Experiment, Workdir, convert_eprofile_analysis
from .utils import CLICK_CONTEXT_SETTINGS, LOG_FORMAT, get_basename, dictval, init_logging, log, TqdmLogHandler, TqdmWrapper


@dataclass
class Screening:
    mgl: MGLToolsWrapper = field(default_factory=MGLToolsWrapper)
    caverdock: CaverDock = field(default_factory=CaverDock)
    threads: Optional[int] = None
    show_progress: bool = True

    def run(self, input_file: str, outdir: str):
        root_logger = logging.getLogger()
        original_log_handlers = list(root_logger.handlers)

        conf = cfggen.build_template_from_file(input_file)

        for screening in conf["screenings"]:
            screening_name = screening['name']
            workdir = Workdir(os.path.join(outdir, dictval(screening, "dir", screening_name.replace(" ", "_"))))
            direction = dictval(screening, "direction", Direction.OUT, lambda x: Direction[x.upper()])
            trajectory_type = dictval(screening, "trajectory_type", TrajectoryType.LOWERBOUND, lambda x: TrajectoryType[x.upper()])
            exhaustiveness = dictval(screening, "exhaustiveness", fn=int)
            seed = dictval(screening, "seed", fn=int)

            analysis_data = pd.DataFrame()
            plots = []

            experiments = Screening._generate_experiments(screening)

            experiment_progress = TqdmWrapper(self.show_progress, lambda: tqdm(total=len(experiments), initial=0, position=0, bar_format="{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}", mininterval=0.00000001, leave=False))
            current_experiment = TqdmWrapper(self.show_progress, lambda: tqdm(total=0, position=1, bar_format="{desc}", leave=False))
            current_step = TqdmWrapper(self.show_progress, lambda: tqdm(total=0, position=2, bar_format="{desc}", leave=False))

            if self.show_progress:
                root_logger.handlers = [h for h in root_logger.handlers if type(h) != logging.StreamHandler]
                root_logger.addHandler(TqdmLogHandler(experiment_progress))

            log.info(f"Running screening {screening_name}")

            for receptor_def, tunnel_def, ligand_def in experiments:
                experiment_progress.tqdm.update(1)
                receptor_path = receptor_def["protein"]
                tunnel_path = tunnel_def if type(tunnel_def) == str else tunnel_def["path"]
                ligand_path = ligand_def if type(ligand_def) == str else ligand_def["path"]

                experiment_name = f"r{get_basename(receptor_path)}-l{get_basename(ligand_path)}-t{get_basename(tunnel_path)}-d{direction.name.lower()}-{trajectory_type.name.lower()}"

                log.info(f"Running experiment {experiment_name}")
                log.info(f"Experiment settings: receptor={receptor_path}, tunnel={tunnel_path}, ligand={ligand_path}, direction={direction.name}, trajectory_type={trajectory_type.name}, seed={seed or '<default>'}, exhaustiveness={exhaustiveness or '<default>'}")
                current_experiment.set_description_str(f"Experiment: {experiment_name}")

                experiment = Experiment(workdir, experiment_name, self.mgl, self.caverdock)
                experiment.store_input_file(receptor_path)
                experiment.store_input_file(ligand_path)
                experiment.store_input_file(tunnel_path)

                current_step.set_description_str(f"Preparing receptor...")
                receptor = Receptor(receptor_path) if receptor_path.endswith(".pdbqt") else experiment.prepare_receptor(receptor_path)

                current_step.set_description_str(f"Preparing ligand...")
                ligand = Ligand(ligand_path) if ligand_path.endswith(".pdbqt") else experiment.prepare_ligand(ligand_path)

                current_step.set_description_str(f"Discretizing tunnel...")
                discretized_tunnel = experiment.discretize_tunnel(
                    tunnel_path, delta=dictval(tunnel_def, "discretization_delta", 0.3, float), threads=self.threads
                )

                extended_tunnel = discretized_tunnel
                ext_distance = dictval(tunnel_def, ["extension", "distance"], 2, float)
                if ext_distance > 0:
                    extended_tunnel = discretized_tunnel + discretized_tunnel.extend(
                        distance=ext_distance, step=dictval(tunnel_def, ["extension", "step"], 0.2, float),
                    )

                current_step.set_description_str(f"Calculating CaverDock...")
                trajectory = experiment.run_caverdock(
                    ligand, receptor, extended_tunnel, direction, trajectory_type,
                    mpi_processes=self.threads,
                    seed=seed,
                    catomnum=dictval(ligand_def, "drag_atom", fn=int),
                    exhaustiveness=exhaustiveness
                )

                eprofile = trajectory.energy_profile
                eprofile.write_to_dat(experiment.result_path("profile.dat"))

                current_step.set_description_str(f"Analysing energy profile...")
                disc_ranges_vals = dictval(tunnel_def, "disc_ranges")
                disc_ranges = None
                if disc_ranges_vals:
                    disc_ranges = DiscRanges(
                        disc_ranges_vals["bound"][0], disc_ranges_vals["bound"][1],
                        disc_ranges_vals["max"][0], disc_ranges_vals["max"][1],
                        disc_ranges_vals["surface"][0], disc_ranges_vals["surface"][1],
                        dictval(screening, "type", DiscRanges.type, lambda x: BoundaryType[x.upper()])
                    )
                analysis = eprofile.analyse(trajectory_type=trajectory_type, disc_ranges=disc_ranges)

                af = convert_eprofile_analysis(experiment_name, analysis, receptor_path, tunnel_path, ligand_path)
                af.to_csv(experiment.result_path("analysis.csv"), index=False)

                analysis_data = pd.concat((analysis_data, af))
                plots.append(EnergyProfilePlot(experiment_name, eprofile, trajectory_type))

            experiment_progress.close()
            current_experiment.close()
            current_step.close()

            if self.show_progress:
                root_logger.handlers = original_log_handlers
                print("\r", end="")

            analysis_data.to_csv(os.path.join(workdir.directory, "results.csv"), index=False)
            log.info("Plotting results")
            plotconf = dictval(screening, "plot", {})
            plot_params = {
                "share_axes": dictval(plotconf, "share_axes", fn=bool),
                "force_active_site_location": dictval(plotconf, "active_site_location", fn=lambda x: ActiveSiteLocation[x.upper()]),
                "lowerbound_color": dictval(plotconf, "lowerbound_color"),
                "upperbound_color": dictval(plotconf, "upperbound_color"),
                "radius_color": dictval(plotconf, "radius_color"),
                "max_plots_per_row": dictval(plotconf, "plots_per_row"),
                "show_zero_energy_line": dictval(plotconf, "show_zero_energy_line"),
                "zero_energy_line_color": dictval(plotconf, "zero_energy_line_color")
            }
            plot_params = {k: v for k, v in plot_params.items() if v is not None}
            plot_results(plots, output=os.path.join(workdir.directory, "out.png"), **plot_params)
            log.info(f"Screening '{screening_name}' successfuly finished!")

        log.info("Screening successfuly finished!")

    @staticmethod
    def _generate_experiments(screening):
        return [
            (receptor, tunnel, ligand)
            for receptor in screening["receptors"]
            for tunnel in receptor["tunnels"]
            for ligand in screening["ligands"]
        ]


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument("screening-yaml", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.option("-o", "--output", help="Output directory to store data",
              type=click.Path(), required=False, default="screening_out")
@click.option("-m", "--mgltools", "mgltools_path", help="Path to MGLTools root directory",
              type=click.Path(exists=True, file_okay=False), required=False)
@click.option("-c", "--caverdock", help="Path to CaverDock binary",
              type=click.Path(exists=True, dir_okay=False), required=False)
@click.option("-p", "--threads", help="Number of threads to use for calculation",
              type=click.IntRange(min=2), required=False)
@click.option("--log", "log_path", help="Log file",
              type=click.Path(dir_okay=False), required=False)
@click.option("--no-progress", help="Hide interactive progress bars. Recommended for non-interactive execution via schedulers.",
              is_flag=True)
@click.option("-v", "--verbose", help="Print also debug log messages",
              is_flag=True)
def cmd(
    screening_yaml: str, output: str, mgltools_path: Optional[str], caverdock: Optional[str], threads: int,
    log_path: Optional[str], no_progress: bool, verbose: bool
):
    init_logging(verbose)

    if log_path:
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        file_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
        logging.getLogger().addHandler(file_handler)

    if not os.path.isdir(output):
        os.mkdir(output)

    try:
        mgl = MGLToolsWrapper(mgltools_path)
    except MGLToolsNotFoundError:
        log.error("Unable to find MGLTools installation! Please set it correctly in your environment or specify it "
                  "manually using -m/--mgltools argument.")
        sys.exit(1)

    try:
        cd = CaverDock(caverdock)
    except CaverDockNotFoundError:
        log.error("Unable to find CaverDock binary! Please add it to your PATH variable or specify it "
                  "manually using -c/--caverdock argument.")
        sys.exit(1)

    Screening(mgl, cd, threads, not no_progress).run(screening_yaml, output)


def main():
    cmd()
