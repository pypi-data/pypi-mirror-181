# PyCaverDock

## Installation instructions

### Clone the repository

```bash
$ git clone <LINK>
```

Copy the `<LINK>` of the repository.

### Prerequisites
1) Download Ubuntu packages
    ```bash
    $ sudo apt-get install -y git python3 python3-pip
    ```

2) Install virtual environment support
    ```bash
    $ pip3 install virtualenv --user
    ```

3) Install CaverDock & MGLTools following the instructions

### Install Python API
Run the following commands in the root directory of the project repository.

1) Create a virtual environment and use it. `<VENV>` is a placeholder for a name of virtual environment.
    ```bash
    $ virtualenv <VENV>
    $ source <VENV>/bin/activate
    ```

2) Install pycaverdock
    ```bash
    $ (<VENV>) pip3 install .
    ```

## Usage of Python API
Look at the pipeline example (`examples/pipeline.py`).

## License
```
MIT License

Copyright (c) 2019- Loschmidt Laboratories & IT4Innovations

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```