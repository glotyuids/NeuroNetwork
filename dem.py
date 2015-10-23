def f(x,a):
    print x(a)

def square(a):
    return a**2

def plus_2(a):
    return a+2

f(square,20)
f(plus_2,20)