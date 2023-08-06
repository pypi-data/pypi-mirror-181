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

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import List, Optional

from .utils import change_cwd, check_path_exists, log


MGLTOOLS_HOME_ENVVAR = "MGLTOOLS_HOME"
PYTHON_SH_PATH = "bin/pythonsh"
SCRIPTS_DIR = "MGLToolsPckgs/AutoDockTools/Utilities24"
PREPARE_RECEPTOR_PATH = os.path.join(SCRIPTS_DIR, "prepare_receptor4.py")
PREPARE_LIGAND_PATH = os.path.join(SCRIPTS_DIR, "prepare_ligand4.py")


@dataclass
class Ligand:
    """
    Represents a ligand stored on disk.
    """
    path: str


@dataclass
class Receptor:
    """
    Represents a receptor stored on disk.
    """
    path: str


class MGLToolsNotFoundError(Exception):
    pass


class MGLToolsWrapper:
    """
    This class wraps the MGLTools package and exposes useful methods for working with it.
    """

    def __init__(self, mgltools_root: Optional[str] = None):
        self.mgltools_root = os.path.abspath(mgltools_root) if mgltools_root else self._autodetect_root()
        check_path_exists(os.path.join(self.mgltools_root, "bin"),
                          "Expected MGLTools directory at", MGLToolsNotFoundError)
        log.debug(f"MGLTools root: {self.mgltools_root}")

    def prepare_receptor(self, receptor: str, output_path: str, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         args: List[str] = None) -> Receptor:
        """
        Prepares an input `receptor` using MGLTools and stores it in `output_path`.

        :param receptor: Path to the input receptor file.
        :param output_path: Output path for the created receptor pdbqt file.
        :param stdout: Standard output stream destination. Valid values are subprocess.PIPE, subprocess.DEVNULL, an existing file descriptor (a positive integer), an existing file object with a valid file descriptor, and None.
        :param stderr: Standard error stream destination. Valid values are subprocess.PIPE, subprocess.DEVNULL, an existing file descriptor (a positive integer), an existing file object with a valid file descriptor, and None.
        :param args: Additional arguments for prepare_receptor.
        """
        check_path_exists(receptor, "Expected receptor file at")

        input_path = os.path.abspath(receptor)

        commands = [
            self.mgltools_path(PYTHON_SH_PATH),
            self.mgltools_path(PREPARE_RECEPTOR_PATH),
            "-r", input_path,
            "-o", output_path
        ]
        if args:
            commands += args
        self.exec(commands, stdout, stderr)
        return Receptor(output_path)

    def prepare_ligand(self, ligand: str, output_path: str, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       args: List[str] = None) -> Ligand:
        """
        Prepares an input `ligand` using MGLTools and stores it in `output_path`.

        :param ligand: Path to the input ligand file.
        :param output_path: Output path for the created ligand pdbqt file.
        :param stdout: Standard output stream destination. Valid values are subprocess.PIPE, subprocess.DEVNULL, an existing file descriptor (a positive integer), an existing file object with a valid file descriptor, and None.
        :param stderr: Standard error stream destination. Valid values are subprocess.PIPE, subprocess.DEVNULL, an existing file descriptor (a positive integer), an existing file object with a valid file descriptor, and None.
        :param args: Additional arguments for prepare_ligand.
        """
        check_path_exists(ligand, "Expected ligand file at")

        input_path = os.path.abspath(ligand)

        commands = [
            self.mgltools_path(PYTHON_SH_PATH),
            self.mgltools_path(PREPARE_LIGAND_PATH),
            "-l", input_path,
            "-o", output_path
        ]
        if args:
            commands += args

        # Workaround for bug in prepare_ligand4.py, it only works with relative paths
        with change_cwd(os.path.dirname(input_path)):
            self.exec(commands, stdout, stderr)
        return Ligand(output_path)

    def mgltools_path(self, path: str) -> str:
        return os.path.join(self.mgltools_root, path)

    def exec(self, args, stdout, stderr):
        log.info(f"Executing MGLTools command {args}")
        return subprocess.run(args, check=True, stdout=stdout, stderr=stderr)

    def _autodetect_root(self):
        home = os.getenv(MGLTOOLS_HOME_ENVVAR)
        if home:
            return home
        home = shutil.which("pythonsh")
        if home:
            try:
                return os.path.dirname(os.path.dirname(home))
            except:
                pass
        raise MGLToolsNotFoundError("Cannot autodetect MGLTools installation from environment. Please specify it explicitly...")
