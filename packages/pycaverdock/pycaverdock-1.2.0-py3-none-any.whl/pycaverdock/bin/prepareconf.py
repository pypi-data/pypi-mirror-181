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

from typing import Optional

from .. import generate_caverdock_config
from ..utils import CLICK_CONTEXT_SETTINGS


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option("-r", "--receptor", help="PDBQT file containing receptor",
              type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("-l", "--ligand", help="PDBQT file containing ligand",
              type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("-t", "--tunnel", help="File containing discretized tunnel",
              type=click.Path(exists=True, dir_okay=False), required=True)
@click.option("-o", "--output", help="Output file",
              type=click.Path(dir_okay=False), required=False)
@click.option("-a", "--drag-atom", help="Ligand drag atom",
              type=click.IntRange(min=0), required=False)
@click.option("--seed", help="Seed",
              type=click.INT, required=False)
@click.option("--exhaustiveness", help="Exhaustiveness",
              type=click.IntRange(min=1), required=False)
def cmd(receptor: str, ligand: str, tunnel: str, output: Optional[str], drag_atom: Optional[int], seed: Optional[int],
        exhaustiveness: Optional[int]):
    """CaverDock config prepare script."""
    config = generate_caverdock_config(ligand, receptor, tunnel, catomnum=drag_atom, seed=seed,
                                       exhaustiveness=exhaustiveness)

    if output:
        with open(output, "w") as fh:
            fh.write(config)
    else:
        print(config)


def main():
    cmd()
