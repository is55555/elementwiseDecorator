# >>> compatibility with Python 3
from __future__ import print_function
import sys

from elementwise import elementwise


@elementwise
def square_e(x):
    return x*x

print(square_e(4))  # prints 16
print(square_e([3, 4, 5]))  # prints [9, 16, 25] <- as a list
print(square_e((3, 5, 6)))  # prints (9, 25, 36) <- as a tuple
print(square_e(set([3, 4, 5])))  # prints set([16, 9, 25]) <-as a set (order may vary)

if sys.version_info < (3,):  # pragma: no cover
    print("Python 2")
    for i in square_e(xrange(11)):  # prints 0 1 4 9 ... does not pre-generate any lists, it executes lazily using the xrange object
        print(i, end=" ")
    print("")
    for j in square_e((i * 2 for i in xrange(11))):  #  0 4 16... also lazily, with a generator comprehension
        print(j, end=" ")
    print("")
    # the following range expands to a list, but the subsequent chained squares are not stored in lists, ...
    # ...but executed lazily thanks to the iterator interface
    for i in square_e(square_e(square_e(iter(range(100))))):
        print(i, end=" ")
else:  # pragma: no cover
    print("Python 3")
    for i in square_e(range(11)):  # prints 0 1 4 9 ... does not pre-generate any lists, it executes lazily using the xrange object
        print(i, end=" ")
    print("")
    for j in square_e((i * 2 for i in range(11))):  #  0 4 16... also lazily, with a generator comprehension
        print(j, end=" ")

    # the following range expands to a list, but the subsequent chained squares are not stored in lists, ...
    # ...but executed lazily thanks to the iterator interface
    for i in square_e(square_e(square_e(range(100)))):
        print(i, end=" ")
