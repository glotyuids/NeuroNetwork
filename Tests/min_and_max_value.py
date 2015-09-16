import random, operator
import math
import time

def f(val,mn=0.2,mx=0.5):
	if val < mn: return mn
	if val > mx: return mx
	return val

def g(val,mn=0.2,mx=0.5):
	return min(max(mn,val),mx)

a = [random.random() for i in xrange(10**7)]

tstart = time.time()
b = [f(i) for i in a]
tend1 = time.time()-tstart
print tend1
b = []
tstart = time.time()
b = [g(i) for i in a]
tend2 = time.time()-tstart
print tend2