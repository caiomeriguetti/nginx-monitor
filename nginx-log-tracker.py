#!/usr/bin/python

from __future__ import with_statement
import re
import json
import datetime
import time

                  # String to find
fname = "/var/log/nginx/teste.log"     # File to check

def tail(f, lines=20 ):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                # from the end of the file
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            # read the last block we haven't yet read
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count('\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = ''.join(reversed(blocks))
    return all_read_text.splitlines()[-total_lines_wanted:]

lines = None

with open(fname, "r") as f:
    lines = tail(f, 5000);

print len(lines)

time_by_request = {}
count_by_request = {}
status_by_request = {}
sum_time = 0.0
log_lines = len(lines)
min_time = None
max_time = None
for line in lines:

	try: 
		linedata = json.loads(line)
	except:
		continue

	duration = float(linedata["duration"])
	
	time = datetime.datetime.strptime(linedata["time_local"].split(" ")[0], "%d/%b/%Y:%H:%M:%S")

	if min_time == None:
		min_time = time
	elif time < min_time:
		min_time = time

	if max_time == None:
		max_time = time
	elif time > max_time:
		max_time = time

	sum_time = sum_time + duration
	request_index = linedata["status"] + " - " + linedata["request"]

	if not(request_index in time_by_request.keys()):
		time_by_request[request_index] = duration
	else:
		time_by_request[request_index] = time_by_request[request_index] + duration

	if not(request_index in count_by_request.keys()):
		count_by_request[request_index] = 1
	else:
		count_by_request[request_index] = count_by_request[request_index] + 1

	
	status_by_request[request_index] = linedata['status']

data = json.dumps({"time_by_request": time_by_request,
									"count_by_request": count_by_request,
									"status_by_request": status_by_request,
									"log_lines": log_lines, 
									"request_time_sum": sum_time,
									"local_time_delta": str(max_time-min_time) })

print data