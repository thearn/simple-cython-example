import numpy as np
from cython_example_proj import array_sum, tessellate
import time

try:  # python2 & python3 compatibility
    xrange
except NameError:
    xrange = range


def array_sum_python(A):
    """
    naive array summation
    """
    m, n = A.shape
    result = 0
    for i in xrange(n):
        for j in xrange(n):
            result += A[i, j]


def tessellate_python(A):
    """
    turns indices of an m by n array into an 2mn by 12 array of triangle
    faces, as per the STL file format.
    """
    m, n = A.shape
    results = np.zeros((2 * m * n, 12))

    for i in xrange(m - 1):
        for k in xrange(n - 1):
            idx = i * n + k
            this_pt = [i, k, A[i, k]]
            top_right = [i, k + 1, A[i, k + 1]]
            bottom_right = [i + 1, k + 1, A[i + 1, k + 1]]
            bottom_left = [i + 1, k, A[i + 1, k]]

            results[idx, 3:6] = top_right
            results[idx, 6:9] = this_pt
            results[idx, 9:] = bottom_right
            results[idx + 1, 3:6] = this_pt
            results[idx + 1, 6:9] = bottom_left
            results[idx + 1, 9:] = bottom_right

    return results

if __name__ == "__main__":

    A = np.random.randn(5000, 5000)
    print(59 * "-")
    print("Initialized array for sum; starting comparison:")
    print(59 * "-")

    t = time.time()
    array_sum(A)
    print("cython finished :", time.time() - t, "s")

    t = time.time()
    A.sum()
    print("numpy finished :", time.time() - t, "s")

    t = time.time()
    array_sum_python(A)
    print("python finished :", time.time() - t, "s")

    print()

    A = np.random.randn(1024, 1024)
    print(59 * "-")
    print("Initialized array for tessellate; starting comparison:")
    print(59 * "-")
    t = time.time()
    tessellate(A)
    print("cython finished :", time.time() - t, "s")

    t = time.time()
    tessellate_python(A)
    print("python+numpy finished :", time.time() - t, "s")
    print()
