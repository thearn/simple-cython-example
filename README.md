simple-cython-example
=======================
[![Build Status](https://travis-ci.org/thearn/simple-cython-example.png?branch=master)](https://travis-ci.org/thearn/simple-cython-example)

A small template project that shows how to wrap C/C++ code into python using [cython](http://cython.org/), and build the extensions into an installable module.

A `.pyx` file is included that implements a few C functions which can accept and return standard
python data types and numpy ndarrays. These are compiled, wrapped, and integrated into the module using a standard `setup.py` script.

In addition to concrete examples of cython syntax, this repo also illustrates a working project structure with a working setup.py configuration (using setuptools)
for Python projects with C extension modules, along with basic unit tests (together with a working Travis-CI config).

# Building
First, install numpy and cython (using pip or from a package manager) if you don't already have them.

Then just run `python setup.py develop` to build the project in-place.

The module (with its wrapped C functions `c_hello`, `factorial`, `array_sum`, and `tessellation`) will then be importable in python:
```bash
>>> from cython_example_proj import c_hello, factorial, array_sum, tessellation
```
# Testing

The test file
[test_cython_examples.py](cython_example_proj/test/test_cython_example.py)
can be run directly, or (if you have nose installed),
can be run automatically by running `nosetests` in the top level directory.

Automated testing is peformed with [Travis CI](https://travis-ci.org/), a free service that integrates with github.
All that is required is to commit a [.travis.yml](.travis.yml) configuration file and mark the repository on your Travis CI account.
Then, each time you push a branch to github, tests will be executed automatically. The results of the tests can be e-mailed
to you. The results of the latest test will be shown at the bottom of every pull request forked from your repository,
and will be reflected in any build status images you embed (like the one at the top of this repo).

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

```
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

So the cython-generated C implementation of `array_sum` is on parity with `numpy.sum`, and are 
are each much faster than the pure python implementation.

The C implementation of `tessellate` blew the python+numpy implementation out of the water. Looks like I've got some
rewriting to do on [STL Tools](https://github.com/thearn/stl_tools)!

# Profiling function
If you're interested in possibily rewriting some or part of a module as a
compiled extension, you should profile the execution of your module first.
The Python standard library module [cProfile](http://docs.python.org/2/library/profile.html) can help you with this.

Unfortunately, sorting the output of cProfile using their API leaves a few options to be desired. Namely: sorting by `percall` time (`cumtime` divided by `ncalls`).

[profile.py](cython_example_proj/profile.py) shows an example of a work-around to this. Re-define the `f()` function to execute functions from your library,
and a profile will be printed, broken down by function, that is sorted by `percall`.


