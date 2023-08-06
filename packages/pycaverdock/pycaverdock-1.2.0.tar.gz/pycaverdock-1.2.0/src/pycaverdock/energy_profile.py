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

import pandas as pd

from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union

from . import Direction, DiscretizedTunnel, TrajectoryType
from .utils import log


@dataclass
class EnergyProfileAnalysis:
    direction: Direction
    trajectory_type: TrajectoryType
    E_bound: float
    E_max: float
    E_surface: float
    k_on: float
    k_off: float
    dE_bs: float


class BoundaryType(Enum):
    DISC_NUMBER = auto()
    FRACTION = auto()


@dataclass
class DiscRanges:
    """
    Definition of Disc ranges for energy profile analysis. Selected parts of profile are used for calculation of important
    energy values.

    :param bound_start: Disc range start for the selection of bound energy in active site.
    :param bound_end: Disc range end for the selection of bound energy in active site.
    :param max_start: Disc range start for the selection of energy maximum in the profile.
    :param max_end: Disc range end for the selection of energy maximum in the profile.
    :param surface_start: Disc range start for the selection of surface energy at the protein surface.
    :param surface_end: Disc range end for the selection of surface energy at the protein surface.
    :param type: Type of range value, DISC_NUMBER for exact disc number, FRACTION for selecting fraction of the profile.
    """
    bound_start: Union[int, float]
    bound_end: Union[int, float]
    max_start: Union[int, float]
    max_end: Union[int, float]
    surface_start: Union[int, float]
    surface_end: Union[int, float]
    type: BoundaryType = BoundaryType.DISC_NUMBER

    def convert(self, direction: Direction, number_of_discs: int):
        boundaries = list(map(
            lambda x: int(number_of_discs * x) if self.type == BoundaryType.FRACTION else x,
            (self.bound_start, self.bound_end, self.max_start, self.max_end, self.surface_start, self.surface_end)
        ))

        if direction == Direction.IN:
            reversed_boundaries = []
            for i in range(0, 6, 2):
                reversed_boundaries.append(number_of_discs - boundaries[i + 1])
                reversed_boundaries.append(number_of_discs - boundaries[i])
            return reversed_boundaries

        return boundaries

    def __post_init__(self):
        assert self.type is not None

        if self.type == BoundaryType.FRACTION:
            assert all(map(lambda x: x >= 0.0 and x <= 1.0, (self.bound_start, self.bound_end, self.max_start, self.max_end, self.surface_start, self.surface_end))), "All boundaries must be between 0.0 and 1.0"
        else:
            assert all(map(lambda x: x >= 0, (self.bound_start, self.bound_end, self.max_start, self.max_end, self.surface_start, self.surface_end))), "All boundaries must be greater or equals than 0"


@dataclass
class EnergyProfile:
    """
    Stores calculated energy profile results in a pandas DataFrame.
    """
    frame: pd.DataFrame
    direction: Direction

    @staticmethod
    def load_from_file(path: str, direction: Direction) -> "EnergyProfile":
        """
        Loads an energy profile from disk.
        """
        data = defaultdict(list)
        with open(path) as f:
            for line in f:
                distance, disk, minE, maxE, radius, lbE = line.strip().split()
                data["distance"].append(float(distance))
                data["disk"].append(int(disk))
                data["minE"].append(float(minE))
                data["maxE"].append(float(maxE))
                data["radius"].append(float(radius))
                data["lbE"].append(float(lbE))
        return EnergyProfile(pd.DataFrame(data), direction)

    def write_to_dat(self, path: str):
        """
        Writes the results to a .dat file.
        """
        with open(path, "w") as f:
            self.write(f)

    def write(self, stream):
        for line in self.frame.itertuples():
            stream.write(
                f"{line.distance} {line.disk} {line.minE} {line.maxE} {line.radius} {line.lbE}\n")

    def reverse(self):
        data = defaultdict(list)
        max_distance = None
        for line in self.frame[::-1].itertuples():
            if max_distance is None:
                max_distance = line.distance
            data["distance"].append(max_distance - line.distance)
            data["disk"].append(line.disk)
            data["minE"].append(line.minE)
            data["maxE"].append(line.maxE)
            data["radius"].append(line.radius)
            data["lbE"].append(line.lbE)
        return EnergyProfile(pd.DataFrame(data), Direction.OUT if self.direction == Direction.IN else Direction.IN)

    def analyse(self, trajectory_type: TrajectoryType = TrajectoryType.LOWERBOUND, disc_ranges: Optional[DiscRanges] = None) -> EnergyProfileAnalysis:
        """
        Calculates E_bound, E_max, E_surface, k_barier, dE_bs and returns the results as a pandas
        Dataframe.

        :param trajectory_type: Type of calculated simulation for energy analysis LOWERBOUND - lowerbound, UPPERBOUND - upperbound profile.
        :param disc_ranges: must be six int or float in precise correct order to set parameters for analysis, see DiscRanges documentation.
        """

        column_key = "maxE" if trajectory_type == TrajectoryType.UPPERBOUND else "lbE"
        data = list(self.frame[column_key])
        number_of_discs = len(data)

        if disc_ranges:
            log.debug("Using custom parameters for Energy profile analysis")
            bound_start, bound_end, max_start, max_end, surface_start, surface_end = disc_ranges.convert(self.direction, number_of_discs)
            E_bound = min(data[bound_start:bound_end])
            E_max = max(data[max_start:max_end])
            E_surface = min(data[surface_start:surface_end])
        else:
            log.debug("Using default parameters for Energy profile analysis")
            if self.direction == Direction.OUT:
                max_start = int(number_of_discs / 10)
                max_end = number_of_discs - 1

                E_bound = min(data[:int(number_of_discs / 2)])
                E_max = max(data[max_start:max_end])
                E_surface = data[number_of_discs - 1]
            else:
                max_end = number_of_discs - int(number_of_discs / 10)

                E_bound = min(data[int(number_of_discs / 2):])
                E_max = max(data[0:max_end])
                E_surface = data[0]

        k_on = round(E_max - E_surface, 1)
        k_off = round(E_max - E_bound, 1)

        dE_bs = E_bound - E_surface
        dE_bs = round(dE_bs, 1)

        return EnergyProfileAnalysis(self.direction, trajectory_type, E_bound, E_max, E_surface, k_on, k_off, dE_bs)


def create_energy_profile(
        tunnel: DiscretizedTunnel,
        caverdock_trajectory: str,
        direction: Direction,
        start_disc: int = 0
) -> EnergyProfile:
    """
    Creates an energy profile from a discretized tunnel and a path to caverdock trajectory results.

    :param tunnel: Object with discretized tunnel.
    :param caverdock_trajectory: Path CaverDock result trajectory pdbqt file.
    :param direction: Direction of the previously calcualted simulation.
    :param start_disc: Disc number where the energy profile generation will start.
    """
    last = []
    dist = 0.0
    disk = 0
    minE = 1000000.0
    maxE = -1000000.0
    lbE = 0.0
    radius = 0.0

    data = defaultdict(list)

    def add_row(dist: float, disk: int, minE: float, maxE: float, radius: float, lbE: float):
        data["distance"].append(dist)
        data["disk"].append(disk - start_disc)
        data["minE"].append(minE)
        data["maxE"].append(maxE)
        data["radius"].append(radius)
        data["lbE"].append(lbE)

    if direction == Direction.IN:
        tunnel = tunnel.reverse()

    with open(caverdock_trajectory) as trfile:
        trline = trfile.readline()
        "#distance disc min UB energy, max UB energy, radius, LB energy"
        for (index, tunnel_disk) in enumerate(tunnel.disks):
            if index < start_disc:
                disk += 1
            else:
                center = tunnel_disk.center
                normal = tunnel_disk.normal
                if not last:
                    last = center
                else:
                    # compute distance between plate of current disc and center of previous disc
                    d = - center[0] * normal[0] - center[1] * normal[1] - center[2] * normal[2]
                    t = -(normal[0] * last[0] + normal[1] * last[1] + normal[2] * last[
                        2] + d) / (
                                normal[0] * normal[0] + normal[1] * normal[1] + normal[2] *
                                normal[2])
                    dist += abs(t)
                    last = center
                # scan snapshots until other disk is reached
                while True:
                    if trline == "":
                        break
                    words = trline.split()
                    trline = trfile.readline()
                    if words[0] == "REMARK" and words[1] == "CAVERDOCK" and words[2] == "RESULT:":
                        valE = float(words[3])
                    if words[0] == "REMARK" and words[1] == "CAVERDOCK" and words[2] == "TUNNEL:":
                        if int(words[3]) > disk - start_disc:
                            add_row(dist, disk, minE, maxE, radius, lbE)
                            minE = valE
                            maxE = valE
                            valE = float(words[4])
                            radius = float(words[5])
                            lbE = float(words[4])
                            break
                        else:
                            maxE = max(maxE, valE)
                            minE = min(minE, valE)
                            radius = float(words[5])
                            lbE = float(words[4])
                disk += 1
        add_row(dist, disk, minE, maxE, radius, lbE)
    return EnergyProfile(pd.DataFrame(data), direction=direction)
