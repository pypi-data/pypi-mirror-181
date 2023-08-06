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

import copy
import math
import multiprocessing

from dataclasses import dataclass
from typing import List, Optional, Tuple

from discretizer.digger import DigOpts, dig_tunnel
from discretizer.io import load_tunnel_from_pdb
from discretizer.tunnel import Tunnel

from .utils import check_path_exists, RedirectStdoutToFile


@dataclass
class Vec3D:
    x: float
    y: float
    z: float

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def __iter__(self):
        yield from self.to_tuple()

    def __getitem__(self, index):
        return self.to_tuple()[index]

    def copy(self):
        return copy.copy(self)


@dataclass
class Disk:
    """
    One disc in the tunnel.
    """
    center: Vec3D
    normal: Vec3D
    radius: float

    def copy(self) -> "Disk":
        return Disk(self.center.copy(), self.normal.copy(), self.radius)


@dataclass
class DiscretizedTunnel:
    """
    Memory representation of the discretized tunnel.

    :param disks: List of discs.
    """
    disks: List[Disk]

    @staticmethod
    def load_from_file(path: str) -> "DiscretizedTunnel":
        """
        Loads a discretized tunnel from a file on the disk.
        Each disk of the tunnel should be stored on a single line, with its values separated by
        space.
        """
        disks = []
        with open(path) as f:
            for line in f:
                items = [float(v) for v in line.strip().split()]
                disks.append(
                    Disk(center=Vec3D(*items[:3]), normal=Vec3D(*items[3:6]), radius=items[6]))

        return DiscretizedTunnel(disks=disks)

    def reverse(self) -> "DiscretizedTunnel":
        """
        Reverse the direction of the tunnel, i.e. the last disk will become the first disk, etc.
        """
        return DiscretizedTunnel(disks=[d.copy() for d in self.disks[::-1]])

    def extend(self, distance: float = 2, step=0.2) -> "DiscretizedTunnel":
        """
        Extends the length of the tunnel in the direction of the vector between the last two tunnel
        dummy atoms.

        :param distance: Length of the extension.
        :param step: Width of the extended discs.
        """
        act = self.disks[-1]
        prev = self.disks[-2]
        normal = act.normal.copy()
        center = act.center.copy()

        direction = [a - p for (a, p) in zip(act.center, prev.center)]

        fit = 1 / math.sqrt(direction[0] ** 2 + direction[1] ** 2 + direction[2] ** 2)

        disks = []
        i = step
        while i <= distance:
            new_center = Vec3D(
                center[0] + (direction[0] * fit * i),
                center[1] + (direction[1] * fit * i),
                center[2] + (direction[2] * fit * i)
            )
            disks.append(Disk(new_center, normal, act.radius))
            i += step
        return DiscretizedTunnel(disks)

    def write_to_file(self, path: str):
        """
        Writes the discretized tunnel to a file on the disk.
        """
        with open(path, "w") as f:
            self.write(f)

    def write(self, stream):
        for disk in self.disks:
            stream.write("{} {} {} {} {} {} {}\n".format(
                disk.center.x, disk.center.y, disk.center.z,
                disk.normal.x, disk.normal.y, disk.normal.z,
                disk.radius)
            )

    def __add__(self, other: "DiscretizedTunnel") -> "DiscretizedTunnel":
        assert isinstance(other, DiscretizedTunnel)
        return DiscretizedTunnel(disks=[d.copy() for d in self.disks + other.disks])


def load_tunnel(path: str) -> Tunnel:
    """
    Loads a (non-discretized) tunnel from a PDB file.
    """
    check_path_exists(path, "Expected tunnel file at")
    return load_tunnel_from_pdb(path)


def discretize_tunnel(
        tunnel: Tunnel,
        delta: float = 0.3,
        threads: Optional[int] = None,
        log: Optional[str] = None
) -> DiscretizedTunnel:
    """
    Discretizes a tunnel using multiple threads.

    :param tunnel: Name of the object with loaded tunnel.
    :param delta: Width of the discretized discs.
    :param threads: Number of maximum threads for running the discretization.
    :param log: Path for optional log file.
    """
    threads = threads or multiprocessing.cpu_count()
    disks = []

    with RedirectStdoutToFile(log):
        # NOTE: filename is None as it is unused
        for disk in dig_tunnel(tunnel, DigOpts(delta, str(None), threads)):
            disks.append(Disk(Vec3D(*disk.center), Vec3D(*disk.normal), disk.radius))

    return DiscretizedTunnel(disks)
