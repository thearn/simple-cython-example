import cProfile
import marshal
import tempfile

"""
Template for writing a library profiler
"""


def f():
    """
    Self-contained profile function for this library

    Compares cython array sum vs. numpy.sum vs. pure python implementation

    Can be used to identify possible areas to re-write as c/c++ extensions
    """
    import numpy as np
    from example_proj import array_sum

    def array_sum2(A):
        m, n = A.shape
        result = 0
        for i in xrange(n):
            for j in xrange(n):
                result += A[i, j]
    A = np.random.randn(5000, 5000)
    array_sum(A)
    A.sum()
    array_sum2(A)


def profile(f, ignore=["f", "<module>"], verbose=True):
    """
    Runs cProfile, gathers function statistics sorted by wall-time per call

    Input:
        f : function to run
        ignore : list of function names to ignore in the output

    Returns:
        vals : list of profiler statistics
                output format:

            [ [method name, number of calls, cumulative time, pertime ] .. ]

                 (sorted by pertime)
    """
    statsfile = tempfile.NamedTemporaryFile()
    cProfile.run('f()', statsfile.name)
    stats = marshal.load(statsfile.file)

    vals = [[key[-1], stats[key][0], stats[key][3],
            stats[key][3] / stats[key][0]] for key in stats
            if key[-1] not in ignore]

    vals.sort(key=lambda x: x[-1])

    if verbose:
        for v in vals:
            print()
            print(v)
    return v

if __name__ == "__main__":
    profile(f)
