import time
from time import strftime, gmtime
tic = time.perf_counter()
time.sleep(1)
toc = time.perf_counter()

t = toc - tic
print(strftime("%H:%M:%S", gmtime(t)))
