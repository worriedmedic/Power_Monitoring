import time

def tail_f(file):
	interval = 1.0

	while True:
		where = file.tell()
		line = file.readline()
		if not line:
			time.sleep(interval)
			file.seek(where)
		else:
			yield line

for line in tail_f(open('/home/pi/Power_Monitoring/data_log/Gateway_Logger.log', 'r'))
	print line
