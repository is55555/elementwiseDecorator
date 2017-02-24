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


# ==========


def every_element(fn):
    def closure(arg):
        if hasattr(arg, "__getitem__"):
            return type(arg)(map(fn, arg))
        elif hasattr(arg, "next") or hasattr(arg, "__next__"):
            res = []
            while True:
                try:
                    x = next(arg)
                    res.append(fn(x))
                except StopIteration:
                    break
            return res
        else:
            return fn(arg)
    return closure


# ==========


def every_element_l(fn):
    def closure(arg):
        if hasattr(arg, "next") or hasattr(arg, "__next__"):
            while True:
                try:
                    x = next(arg)
                    yield(fn(x))
                except StopIteration:
                    break
    return closure


@every_element
def square(x):
    return x*x


@every_element_l
def square_l(x):
    return x*x


@elementwise
def square_e(x):
    return x*x


print square(4)
print square([3,4,5])
print square((3,5,6))

print "?", square(iter(range(200)))

print square((i * 2 for i in xrange(10)))

# for j in square_l((i * 2 for i in xrange(100000000))):
for j in square_l((i * 2 for i in xrange(11))):
        print j

print "elementwise"



print "_____"


print square_e(4)
print square_e([3,4,5])
print square_e((3,5,6))

for i in square_e(square_e(square_e(iter(range(200))))):
    print i,

print ""

print "*", square_e([i * 2 for i in xrange(10)])

for j in square_e((i * 2 for i in xrange(11))):
    print j

print set([3,4,5])
print square_e(set([3,4,5]))

for i in square_e(xrange(11)):
    print i,