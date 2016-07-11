

def integrate_f(double a, double b, int N):
    cdef int i
    cdef double s, dx
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += (i+dx)
    return s * dx

def say_hello():
    print "Hello Cython!"