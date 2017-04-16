import sys


def propagate_iter(fn, it):
    while True:
#        yield fn(it.next())  #  deprecated
        yield fn(next(it))  # this works in Python 3 and also in Python 2 (2.6+)


# xrange does not have a .next() method
def propagate_xrange(fn, xr):
    for i in xr:
        yield fn(i)


def elementwise(fn):
    def closure(arg):
        if sys.version_info < (3,) and type(arg) == xrange:
            # must come first because xrange actually has __getitem__
            return propagate_xrange(fn, arg)
        elif hasattr(arg, "next") or hasattr(arg, "__next__"):
            return propagate_iter(fn, arg)
        elif sys.version_info >= (3,) and isinstance(arg, range):
            arg_it = iter(arg)
            return propagate_iter(fn, arg_it)
        elif type(arg) == set:
            return set(map(fn, arg))
        elif hasattr(arg, "__getitem__"):
            return type(arg)(map(fn, arg))
        else:
            return fn(arg)
    return closure


def elementwise_old(fn):
    def closure(arg):
        if sys.version_info < (3,) and type(arg) == xrange:
            # must come first because xrange actually has __getitem__
            return propagate_xrange(fn, arg)
        elif hasattr(arg, "__getitem__"):
            return type(arg)(map(fn, arg))
        elif hasattr(arg, "next") or hasattr(arg, "__next__"):
            return propagate_iter(fn, arg)
        elif type(arg) == set:
            return set(map(fn, arg))
        else:
            return fn(arg)
    return closure

