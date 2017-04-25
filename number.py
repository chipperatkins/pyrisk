from datetime import datetime 
import time
start = datetime.now()
def check():
	f = open('output.txt','r')
	c = 0
	for line in f:
		for word in line.split():
			if word == 'Outcome':
				c += 1
	print c, datetime.now() - start

while(True):
	check()
	time.sleep(15)
