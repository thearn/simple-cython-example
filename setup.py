from setuptools import setup, Extension
# Use Cython.Build instead of Cython.Distutils
from Cython.Build import build_ext
import numpy as np

# Define the source directory relative to setup.py
SRC_DIR = "cython_example_proj"

# Define the Cython extension
ext_1 = Extension(
    SRC_DIR + ".wrapped",
    [SRC_DIR + "/lib/cfunc.c", SRC_DIR + "/wrapped.pyx"],
    libraries=[],
    include_dirs=[np.get_include()]
)

EXTENSIONS = [ext_1]

# Setup configuration focused only on building the extension
# Remove the __name__ == "__main__" guard
setup(
    # Removed packages and package_dir
    cmdclass={"build_ext": build_ext},
    ext_modules=EXTENSIONS
)
