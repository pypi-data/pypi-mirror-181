# coding=utf-8

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

from setuptools import find_packages, setup

DESCRIPTION="""CaverDock is a software tool for rapid analysis of transport processes in proteins. It models the transportation of a ligand - a substrate, a product, an inhibitor, a co-factor or a co-solvent - from outside environment into the protein active or binding site and vice versa.

The current version of CaverDock uses Caver for pathway identification and heavily modified Autodock Vina as a docking engine. The tool is much faster than molecular dynamic simulations (2-20 min per job), making it suitable even for virtual screening. The software is extremely easy to use as it requires in its minimalistic configuration the setup for AutoDock Vina and geometry of the tunnel.

This API wraps all calculation steps to Python functions and enables the users to construct customized high throughput analysis pipelines."""

with open("requirements.txt") as reqs:
    requirements = reqs.read().splitlines(keepends=False)

setup(
    name="pycaverdock",
    # IMPORTANT: The major and minor version of pyCaverDock should be in alignment with major and minor version of the CaverDock to ensure compatibility.
    version="1.2.0",
    author="CaverDock team",
    author_email="caver@caver.cz",
    url="https://loschmidt.chemi.muni.cz/caverdock",
    description="Python API for CaverDock",
    long_description=DESCRIPTION,
    keywords=["CaverDock", "protein", "tunnel", "docking", "ligand"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: POSIX",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    entry_points={
        "console_scripts": [
            "cd-analysis=pycaverdock.bin.analysis:main",
            "cd-analyseeprofile=pycaverdock.bin.analyseeprofile:main",
            "cd-energyprofile=pycaverdock.bin.energyprofile:main",
            "cd-extendtunnel=pycaverdock.bin.extendtunnel:main",
            "cd-prepareconf=pycaverdock.bin.prepareconf:main",
            "cd-reverseeprofile=pycaverdock.bin.reverseeprofile:main",
            "cd-screening=pycaverdock.screening:main"
        ],
    }
)
