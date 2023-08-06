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

import logging
import os
import sys

from contextlib import contextmanager
from tqdm import tqdm
from typing import Type


LOG_FORMAT = "[%(asctime)s] %(message)s"
log = logging.getLogger("pycaverdock")

CLICK_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], show_default=True)


class FileNotFoundError(Exception):
    pass


class TqdmLogHandler(logging.Handler):

    def __init__(self, dest):
        logging.Handler.__init__(self)
        self.dest: tqdm = dest
        self.formatter = logging.Formatter(LOG_FORMAT)

    def emit(self, record):
        msg = self.format(record)
        self.dest.write(msg)


class TqdmWrapper:

    def __init__(self, enabled, tqdm_create_fn):
        self.tqdm: tqdm = tqdm_create_fn() if enabled else None

    def set_description_str(self, msg):
        if self.tqdm is not None:
            self.tqdm.set_description_str(msg)

    def write(self, msg):
        if self.tqdm is not None:
            self.tqdm.write(msg)

    def refresh(self):
        if self.tqdm is not None:
            self.tqdm.refresh()

    def close(self):
        if self.tqdm is not None:
            self.tqdm.close()

    def update(self, n):
        if self.tqdm is not None:
            self.tqdm.update(n)


class RedirectStdoutToFile:

    def __init__(self, file: str = None):
        self.file = file

    def __enter__(self):
        if self.file is None:
            return self

        self._stdout = sys.stdout
        sys.stdout = self._io = open(self.file, 'w')
        return self

    def __exit__(self, *args):
        if self.file is None:
            return self

        self._io.close()
        del self._io    # free up some memory
        sys.stdout = self._stdout

    def flush(self):
        pass


@contextmanager
def change_cwd(path: str):
    original_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_cwd)


def check_path_exists(path: str, error_msg: str, error_class: Type[Exception] = FileNotFoundError):
    if not os.path.exists(path):
        raise error_class(f"{error_msg} {path}")


def get_basename(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def get_extension(path: str) -> str:
    return os.path.splitext(path)[1]


def ensure_dir(path: str):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)


def dictval(dictionary, key, default=None, fn=None):
    if type(dictionary) != dict:
        return default

    val = dictionary
    if type(key) == list:
        for k in key:
            if type(val) != dict:
                return default

            if k in val:
                val = val[k]
            else:
                return default
    else:
        if key in dictionary:
            val = dictionary[key]
        else:
            return default

    return fn(val) if fn else val


@contextmanager
def noop():
    yield None


def init_logging(verbose: bool = False) -> None:
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO, format=LOG_FORMAT)
