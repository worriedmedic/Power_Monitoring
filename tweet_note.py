import time

def follow(thefile):
	thefile.seek(0,2) # Go to the end of the file
	while True:
		line = thefile.readline()
		if not line:
			time.sleep(0.1) # Sleep briefly
			continue
		yield line

logfile = open("access-log")
loglines = follow(logfile)

for line in loglines:
	print line
