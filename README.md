simple-cython-example
=======================

A small template project that acts as a working tutorial on how to wrap C
code into python using [cython](http://cython.org/), and integrate the
extensions into an installable module. This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. This repository serves as a practical example of integrating Cython-compiled C extensions into a Python project managed with Poetry.

[A cython pyx file](cython_example_proj/wrapped.pyx) is included that implements a few C functions which can accept
and return standard
python data types and numpy ndarrays. These are compiled, wrapped, and
integrated into the module using [Cython](http://cython.org/) and `setuptools`, orchestrated by Poetry via the `pyproject.toml` and a minimal `setup.py` script (using a `build.py` entry point specified in `pyproject.toml`).

In addition to concrete examples of cython syntax, this repo also illustrates
a working project structure for Python projects with C extension modules using Poetry, along with basic unit tests.

## Setup, Building, and Testing with Poetry

### Installation & Initial Build
First, ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed.

Then, navigate to the project root directory and run:
```bash
poetry install
```
This command performs several actions:
1. Creates a dedicated virtual environment for the project (if one doesn't already exist).
2. Installs all Python dependencies listed in `pyproject.toml` (like `numpy`, `cython`, `pytest`).
3. Automatically triggers the build process for the Cython extension (defined in `setup.py` and configured via `build.py` in `pyproject.toml`), making the compiled C functions available to the Python code.

After installation, the module and its wrapped C functions (`c_hello`, `factorial`, `array_sum`, `tessellation`) are importable within the Poetry environment:
```python
# Example usage within the Poetry environment (e.g., using 'poetry run python')
from cython_example_proj import c_hello, factorial, array_sum, tessellation

c_hello() # Prints "hello from C"
print(f"Factorial of 5: {factorial(5)}")
# ... etc.
```

### Rebuilding the Extension (Development)
If you modify the Cython (`.pyx`) or C (`.c`, `.h`) source files, you'll need to rebuild the extension without reinstalling all dependencies. Use the following command:
```bash
poetry run python setup.py build_ext --inplace
```
This compiles the changes and updates the shared object file (`.so` or `.pyd`) directly in the source tree.

### Running Tests
To run the unit tests, execute:
```bash
poetry run pytest cython_example_proj
```
The tests are located in `cython_example_proj/test/test_cython_examples.py` and verify the correctness of the wrapped Cython functions:
*   `test_c_hello`: Checks if the wrapped C `hello()` function executes without error (implicitly checks linking).
*   `test_factorial`: Validates the `factorial` function against known results for several inputs.
*   `test_array_sum`: Ensures the `array_sum` function correctly sums elements of a sample NumPy array.
*   `test_tessellate`: Checks the output shape and potentially some values of the `tessellate` function for a sample input array.

## Wrapped example functions

4 examples functions are defined in
[wrapped.pyx](cython_example_proj/wrapped.pyx):

- A direct wrapping of a simple C "hello world" function, implemented in [cfunc.c](cython_example_proj/lib/cfunc.c)
- A C function to compute the factorial of a python integer, built using
    Cython syntax
- A C function to compute the sum of a numpy ndarray
- A C function to compute and return the tessellation structure (ndarray)
  of the pixels of an inputted digital image (ndarray). This is a re-implementation of first half of the main method used in the [STL Tools](https://github.com/thearn/stl_tools) library.

# Benchmarks

For a quick benchmark of the two ndarray functions listed, run:
```bash
poetry run python timings.py
```
This will execute the `timings.py` script within the Poetry-managed environment and show timings of the wrapped C functions vs. numpy+python and/or pure python implementations of the same functions.

```
-----------------------------------------------------------
Initialized array for sum; starting comparison:
-----------------------------------------------------------
cython finished : 0.0239799022675 s
numpy finished : 0.024649143219 s
python finished : 14.2366518974 s

-----------------------------------------------------------
Initialized array for tessellate; starting comparison:
-----------------------------------------------------------
cython finished : 0.3423628807067871 s
python+numpy finished : 48.1245310307 s

```

So the cython-generated C implementation of `array_sum` is on parity with `numpy.sum`, and are
are each much faster than the pure python implementation.

The C implementation of `tessellate` is much faster than the python+numpy implementation. Using this information,
I've written a complete c-extension for [STL Tools](https://github.com/thearn/stl_tools).

# Profiling function
If you're interested in possibily rewriting some or part of a module as a
compiled extension, you should profile the execution of your module first.
The Python standard library module [cProfile](http://docs.python.org/2/library/profile.html) can help you with this.

Unfortunately, sorting the output of cProfile using their API leaves a few options to be desired. Namely: sorting by `percall` time (`cumtime` divided by `ncalls`).

[profile.py](cython_example_proj/profile.py) shows an example of a work-around to this. Re-define the `f()` function to execute functions from your library,
and a profile will be printed, broken down by function, that is sorted by `percall`.
