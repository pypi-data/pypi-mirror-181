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

import sys

import click

from .. import Direction, DiscretizedTunnel, create_energy_profile
from ..utils import CLICK_CONTEXT_SETTINGS


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option("-d", "--tunnel", help="File containing discretized tunnel",
              type=click.Path(exists=True), required=True)
@click.option("-t", "--trajectory", help="File containing output CaverDock trajectory",
              type=click.Path(exists=True), required=True)
@click.option("-s", "--start", help="Starting disc",
              type=click.IntRange(min=0), required=False, default=0)
@click.option("-r", "--direction", help="Direction",
              type=click.Choice([d.name for d in Direction], case_sensitive=False), required=False,
              default=Direction.OUT.name)
def cmd(tunnel: str, trajectory: str, direction: str, start: int):
    """Energy profile generator"""
    tunnel = DiscretizedTunnel.load_from_file(tunnel)
    profile = create_energy_profile(tunnel, trajectory, Direction[direction], start_disc=start)
    profile.write(sys.stdout)


def main():
    cmd()
