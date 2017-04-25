import subprocess
import sys
from datetime import datetime

procs = []
startTime = datetime.now()
for i in range(32):
	proc = subprocess.Popen([sys.executable, 'pyrisk.py', '--nocurses', '-l', '-g 32', 'AlAI', 'ChronSearchAI', 'StupidAI', 'ChronAI'])
	procs.append(proc)

for proc in procs:
	proc.wait()

print datetime.now() - startTime
execfile('addUp.py')
