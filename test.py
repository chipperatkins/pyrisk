import subprocess
import sys

procs = []
for i in range(2):
	proc = subprocess.Popen([sys.executable, 'pyrisk.py', '--nocurses', '-l', '-g 5', 'StupidAI', 'ClusterAI', 'StupidAI', 'StupidAI'])
	procs.append(proc)

for proc in procs:
	proc.wait()
