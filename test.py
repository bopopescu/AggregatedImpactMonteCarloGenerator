import time
from multiprocessing import Pool
from numpy import random
from numpy.linalg import inv
import time
import threading

n = 500
 

def func(i):
	A=random.random((n,n))
	iA=inv(A)


class funcThread(threading.Thread):
 
	def __init__(self):
 
		threading.Thread.__init__(self)
 
	def run(self):
		# notre fonction
			A=random.random((n,n))
			iA=inv(A)		

t0 = time.time()
 
# va stocker les threads qu'on va lancer.
threadList = []
 
for i in xrange(100) :	# on lance cent milles threads
 
	curThread = funcThread()
	curThread.start()	# on lance le thread
	threadList.append(curThread)	# on ajoute le thread a la list

print time.time() - t0

raw_input()


# timer
t0 = time.time()

pool = Pool()
asyncResult = pool.map_async(func, xrange(100))	# on lance aussi cent milles operations
resultList = asyncResult.get()	# asyncResult.get() is a list of values
print time.time() - t0

raw_input()
