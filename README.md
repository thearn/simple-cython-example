
simple-cython-example
=======================
A small template project that shows how to wrap C/C++ code into python using Cython, and build the extensions into an installable module.

A `.pyx` file is included that implements a few wrapped C functions which can accept and return standard
python data types and numpy ndarrays.

In addition to concrete examples of cython syntax, this repo also illustrates a working project structure with a working setup.py configuration (using setuptools)
for Python projects with C extension modules, and unit test (with a working Travis-CI config).

# Building
First, install numpy and cython.

Run `python setup.py develop` to build the project in-place.

Several wrapped C functions will then be importable under the package
`cython_example_proj`.

The unit test file
[test_cython_examples.pyx](cython_example_proj/test/test_cython_example.py)
can be run directly, or (if you have nose installed).
can be run automatically by running `nosetests` in the top level directory.
`nosetests` is a command that will run any unit tests that it can find in the current directory/subdirectories.

# Wrapped example functions

4 examples functions are defined in
[wrapped.pyx](cython_example_proj/wrapped.pyx):

- A direct wrapping of a simple C "hello world" function, implemented in [cfunc.c](cython_example_proj/lib/cfunc.c)
- A C function to compute the factorial of a python integer, built using
    Cython syntax
- A C function to compute the sum of a numpy ndarray
- A C function to compute and return the tessellation structure (ndarray)
  of the pixels of an inputted digital image (ndarray). This is a re-implementation of the main method used in the [STL Tools](https://github.com/thearn/stl_tools) library.

# Benchmarks

For a quick benchmark of the two ndarray functions listed, run
`python timings.py`. This will show timings of the wrapped C functions
vs. numpy+python and/or pure python implementations of the same functions.

```bash
-----------------------------------------------------------
Initialized array for sum; starting comparison:
-----------------------------------------------------------
cython finished : 0.0239799022675 s
numpy finished : 0.024649143219 s
python finished : 14.2366518974 s

-----------------------------------------------------------
Initialized array for tesselate; starting comparison:
-----------------------------------------------------------
cython finished : 2.98883199692 s
python+numpy finished : 48.1245310307 s

```

So the cython-generated C implementation of `array_sum` is interestingly on parity with `numpy.sum`, which
are together much faster than the pure python implementation.

The C implementation of `tessellatee` blew a python+numpy implementation out of the water.

# Profiling function
If you're interested in possibily rewriting some or part of a module as a
compiled extension, you should profile the execution of your module first.
The Python standard library module [cProfile](http://docs.python.org/2/library/profile.html) can help you with this.

Unfortunately, sorting the output of cProfile using their API leaves a few options to be desired. Namely: sorting by `percall` time (`cumtime` divided by `ncalls`).

[profile.py](cython_example_proj/profile.py) shows an example of a work-around to this. Re-define the `f()` function to execute functions from your library,
and a profile will be printed, broken down by function, that is sorted by `percall`.


