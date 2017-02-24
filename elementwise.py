def propagate_iter(fn, it):
    while True:
        yield fn(it.next())


# xrange does not have a .next() method
def propagate_xrange(fn, xr):
    for i in xr:
        yield fn(i)


def elementwise(fn):
    def closure(arg):
        if type(arg) == xrange: # must come first because xrange actually has __getitem__
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

