cimport cython
import numpy as np
cimport numpy as np

DTYPE = np.float
ctypedef np.float_t DTYPE_t

# This file shows 4 examples:
#   - Wrapping an external c function into python, "c_hello"
#   - Making a wrapped c function on python types w/ cython syntax, "factorial"
#   - A c function that takes an ndarray array and returns a scalar, "array_sum"
#   - A c function that takes an ndarray and returns an ndarray "tesselation"

cdef extern from "lib/cfunc.h":
    # Imports definitions from a c header file
    # Corresponding source file (cfunc.c) must be added to
    # the extension definition in setup.py for proper compiling & linking

    void hello()


def c_hello():
    # Exposes a c function to python

    hello()


def factorial(int x):
    # Basic example of a cython function, which defines
    # python-like operations and control flow on defined c types

    cdef int m = x
    cdef int i

    if x <= 1:
        return 1
    else:
        for i in range(1, x):
            m = m * i
        return m

# decorator turns off bounds-checking for speed
@cython.boundscheck(False)
def array_sum(double[:, ::1] A):
    # example of an ndarray function that returns a scalar
    cdef int m = A.shape[0]
    cdef int n = A.shape[1]
    cdef unsigned int i, j  # iteration variables should be unsigned for speed
    cdef double result = 0

    for i in range(m):
        for k in range(n):
            result += A[i, k]

    return result


@cython.boundscheck(False)
def tessellate(double[:, ::1] A):
    # example of array function that returns a new ndarray
    # turns indices of an m by n array into an 2mn by 12 array of triangle
    # faces, as per the STL file format.

    cdef int m = A.shape[0]
    cdef int n = A.shape[1]
    cdef int i, j, idx
    cdef double i_ = 0
    cdef double k_ = 0

    cdef double[:, ::1] results = np.zeros([2 * m * n, 12])

    for i in range(m - 1):
        for k in range(n - 1):
            idx = <unsigned int> i * n + k

            results[idx, 3] = i_
            results[idx, 4] = k_ + 1
            results[idx, 5] = A[i, k + 1]

            results[idx, 6] = i_
            results[idx, 7] = k_
            results[idx, 8] = A[i, k]

            results[idx, 9] = i_ + 1
            results[idx, 10] = k_ + 1
            results[idx, 11] = A[i + 1, k + 1]

            results[idx + 1, 3] = i_
            results[idx + 1, 4] = k_
            results[idx + 1, 5] = A[i, k]

            results[idx + 1, 6] = i_ + 1
            results[idx + 1, 7] = k_
            results[idx + 1, 8] = A[i + 1, k]

            results[idx + 1, 9] = i_ + 1
            results[idx + 1, 10] = k_ + 1
            results[idx + 1, 11] = A[i + 1, k + 1]

            i_ += 1
            k_ += 1

    return results
