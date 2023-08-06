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

from .. import DiscretizedTunnel
from ..utils import CLICK_CONTEXT_SETTINGS


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option("-f", "--file", help="File containing discretized tunnel",
              type=click.Path(exists=True), required=True)
@click.option("-d", "--distance", help="Distance (in Angstroms) of th extension",
              type=click.FloatRange(min_open=0), required=False, default=2)
@click.option("-s", "--step", help="Step (in Angstroms) of the extension",
              type=click.FloatRange(min_open=0), required=False, default=.2)
@click.option("-o", "--output", help="Output file",
              type=click.Path(dir_okay=False, writable=True), required=False)
def cmd(file: str, distance: float, step: float, output: Optional[str]):
    """Tunnel extender."""
    tunnel = DiscretizedTunnel.load_from_file(file)
    extended = tunnel.extend(distance=distance, step=step)

    if output:
        extended.write_to_file(output)
    else:
        extended.write(sys.stdout)


def main():
    cmd()
