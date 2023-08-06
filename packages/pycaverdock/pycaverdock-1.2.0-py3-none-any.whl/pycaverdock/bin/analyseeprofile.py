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
import csv
import sys

from typing import List, Optional

from .. import BoundaryType, DiscRanges, Direction, EnergyProfile, EnergyProfileAnalysis, TrajectoryType
from ..utils import CLICK_CONTEXT_SETTINGS


def _write_results(files, results, stream, no_header):
    w = csv.DictWriter(stream, fieldnames=["file", "E_bound", "E_max", "E_surface", "k_on", "k_off", "dE_bs"], extrasaction="ignore")

    if not no_header:
        w.writeheader()

    for i in range(len(files)):
        row = dict(results[i].__dict__)
        row["file"] = files[i]
        w.writerow(row)


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument("energy-profiles", nargs=-1, type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("-d", "--direction", help="Direction",
              type=click.Choice([d.name for d in Direction], case_sensitive=False), required=False,
              default=Direction.OUT.name)
@click.option("-s", "--trajectory-type", help="Trajectory type",
              type=click.Choice([d.name for d in TrajectoryType], case_sensitive=False), required=False,
              default=TrajectoryType.LOWERBOUND.name)
@click.option("-o", "--output", help="Output file",
              type=click.Path(dir_okay=False), required=False)
@click.option("-b", "--boundary-type", help="Type of boundary",
              type=click.Choice([d.name for d in BoundaryType], case_sensitive=False), required=False,
              default=BoundaryType.DISC_NUMBER.name)
@click.option("--bound-start", help="Start boundary for bound energy",
              type=click.STRING, required=False)
@click.option("--bound-end", help="End boundary for bound energy",
              type=click.STRING, required=False)
@click.option("--max-start", help="Start boundary for max energy",
              type=click.STRING, required=False)
@click.option("--max-end", help="End boundary for max energy",
              type=click.STRING, required=False)
@click.option("--surface-start", help="Start boundary for surface energy",
              type=click.STRING, required=False)
@click.option("--surface-end", help="End boundary for surface energy",
              type=click.STRING, required=False)
@click.option("-a", "--append", help="Append results to output file",
              is_flag=True)
@click.option("--no-header", help="Do not print header to output file. Suitable when appending.",
              is_flag=True)
def cmd(energy_profiles: List[str], direction: str, trajectory_type: str, output: Optional[str], boundary_type: str, bound_start: Optional[str], bound_end: Optional[str], max_start: Optional[str], max_end: Optional[str], surface_start: Optional[str], surface_end: Optional[str], append: bool, no_header: bool):
    """CaverDock analyse energy profile script."""
    boundaries = dict(bound_start=bound_start, bound_end=bound_end, max_start=max_start, max_end=max_end, surface_start=surface_start, surface_end=surface_end)
    has_boundaries = any(boundaries.values())
    if has_boundaries:
        if not all(boundaries.values()):
            print("All or none boundaries must be specified!")
            sys.exit(1)

        boundary_type = BoundaryType[boundary_type]
        boundary_conversion_fn = int if boundary_type == BoundaryType.DISC_NUMBER else float
        try:
            boundaries = {k: boundary_conversion_fn(v) for k, v in boundaries.items()}
        except ValueError:
            print("Boundaries must be either integers (for discs) or floats (for distances)")
            sys.exit(1)
        boundaries["type"] = boundary_type

    data = []

    for eprofile_path in energy_profiles:
        data.append(EnergyProfile.load_from_file(eprofile_path, Direction[direction]).analyse(trajectory_type, DiscRanges(**boundaries) if has_boundaries else None))


    if output:
        with open(output, "a" if append else "w") as fh:
            _write_results(energy_profiles, data, fh, no_header)
    else:
        _write_results(energy_profiles, data, sys.stdout, no_header)


def main():
    cmd()
