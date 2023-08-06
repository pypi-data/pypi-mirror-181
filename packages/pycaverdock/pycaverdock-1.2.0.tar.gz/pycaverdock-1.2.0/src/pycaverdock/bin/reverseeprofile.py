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
import sys

from typing import Optional

from .. import Direction, EnergyProfile
from ..utils import CLICK_CONTEXT_SETTINGS


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.argument("energy-profile", nargs=1, type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("-o", "--output", help="Output file",
              type=click.Path(dir_okay=False), required=False)
def cmd(energy_profile: str, output: Optional[str]):
    """CaverDock reverse energy profile script."""
    eprofile = EnergyProfile.load_from_file(energy_profile, Direction.IN).reverse()

    if output:
        eprofile.write_to_dat(output)
    else:
        eprofile.write(sys.stdout)


def main():
    cmd()
