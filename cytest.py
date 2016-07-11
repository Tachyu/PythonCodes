import math  
import Cython
import time
from cython_t import say_hello
from cython_t import integrate_f


def integrate_f_py(a,  b,  N):
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += (i+dx)
    return s * dx

say_hello()
start = time.clock()
print integrate_f_py(12,11,100)
end1 = time.clock()
print integrate_f(12,11,100)
end2 = time.clock()

print "cython:" + str(end2 - end1)
print "python:" + str(end1 - start)
print "acc:" + str((end1 - start)/(end2 - end1) - 1)