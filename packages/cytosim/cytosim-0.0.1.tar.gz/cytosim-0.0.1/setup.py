# Test
"""Cytosim: Langevin dynamics of active polymer networks

Cytosim is a simulation tool for cytoskeleton and polymers.
"""
# setup.py stolen from mem3dg : https://github.com/RangamaniLabUCSD/Mem3DG
import os
import sys
import subprocess
import re
version = "0.0.1"
cmake_args=[]

if('CONDA_PREFIX' in os.environ):
    print("Setting library search path (CMAKE_PREFIX_PATH): %s"%(os.environ['CONDA_PREFIX']))
    cmake_args.append('-DCMAKE_PREFIX_PATH=%s'%(os.environ['CONDA_PREFIX']))

DOCLINES = __doc__.split("\n")

CLASSIFIERS = """\
Development Status :: 3 - Alpha
Environment :: Console
Intended Audience :: Science/Research
License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)
Natural Language :: English
Operating System :: OS Independent
Programming Language :: C++
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Scientific/Engineering :: Chemistry
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Physics
Topic :: Scientific/Engineering :: Visualization
"""

try:
    from skbuild import setup
except ImportError:
    print('\nERROR: scikit-build is required to build from source.', file=sys.stderr)
    print('Please run:', file=sys.stderr)
    print('', file=sys.stderr)
    print('  python -m pip install scikit-build\n', file=sys.stderr)
    print('  -- or --\n', file=sys.stderr)
    print('  conda install scikit-build', file=sys.stderr)
    sys.exit(1)

from setuptools import find_packages

setup(
    name="cytosim",
    version=version,
    #packages=find_packages(where="python_src"),
    #package_dir={"": "python_src"},
    #cmake_install_dir="build",
    #include_package_data=True,
    #extras_require={"test": ["pytest"]},
    #packages=find_packages(where="src/tools"),
    packages=find_packages(where="module"),
    package_dir={"": "module"},
    cmake_install_dir="module",
    description=DOCLINES[0],
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    platforms=["Windows", "Linux", "Mac OS-X", "Unix"],
    #classifiers=[c for c in CLASSIFIERS.split("\n") if c],
    keywords="simulation actin microtubule polymer",
    cmake_args=cmake_args,
    zip_safe=False,
)