# Elementwise decorator
(Tried and tested in Python 2.7 and Python 3.6)

Implements element-wise mapping as in the R language, NumPy, or Maple among others: preserving the type of the sequence being iterated over (unlike Python's native map(fn, seq) function).


Usage:

    from elementwise import elementwise

    @elementwise
    def square_e(x):
        return x*x

    print square_e(4) # prints 16
    print square_e([3,4,5]) # prints [9, 16, 25] <- as a list
    print square_e((3,5,6)) # prints (9, 25, 36) <- as a tuple
    print square_e(set([3,4,5])) # prints set([16, 9, 25]) <-as a set (order may vary)
    for i in square_e(xrange(11)): # prints 0 1 4 9 ... does not pre-generate any lists, it executes lazily using the xrange object
        print i,
    print ""
    for j in square_e((i * 2 for i in xrange(11))): #  0 4 16... also lazily, with a generator comprehension
        print j,


    # the following range expands to a list, but the subsequent chained squares are not stored in lists, ...
    # ...but executed lazily thanks to the iterator interface
    for i in square_e(square_e(square_e(iter(range(200))))):
        print i,

# Some notes on implementation

The following simple decorator would work on lists, tuples and single elements:

    def elementwise(fn):
        def closure(arg):
            if hasattr(arg, "__getitem__"):
                return type(arg)(map(fn, arg))
            else:
                return fn(arg)
        return closure

Including iterators is a bit trickier. If we wanted to simply precompute into a list, the following modification would work just fine:

    def elementwise(fn):
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

However, that's not what we generally want when we use iterators. We want to allow lazy execution of the function through each element.
The following would work just for iterators, taking in and passing out an iterator:

    def lazy_exec_elementwise_just_for_iterators(fn):
        def closure(arg):
            if hasattr(arg, "next") or hasattr(arg, "__next__"):
                while True:
                    try:
                        x = next(arg)
                        yield(fn(x))
                    except StopIteration:
                        break
        return closure

Now the problem is that in Python 2 we cannot combine yield and return in the same function. In the decorator provided, I work around this using a function to propagate the iterator (see code) and then I also added a similar function to also work on xrange objects, which are not compatible otherwise. I also added set to the interface since this was simple enough and made sense.

For the time being I decided not to add dictionaries, because in the general case it makes little sense to map functions to the values ignoring the keys, and there is no general case that really deserves inclusion.

# Installation

Simply include the corresponding file, it has no dependencies.

# Licence

MIT