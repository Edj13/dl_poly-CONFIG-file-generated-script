import numpy as np
from math import *
import sys
import copy
import random

filename = sys.argv[1]
filename_to = sys.argv[2]
writefile = []
record_i = []
record_i_buffer1 = []
record_i_buffer2 = []
check = 'False'
mark = False
buffer_width = float(sys.argv[3])
number = 0

with open(filename,'r') as f:
	for i,line in enumerate(f):
		if i == 1:
			keytrj = int(line.split()[0])

with open(filename,'r') as f:
	for i, line in enumerate(f):
		if i == 2:
			sidelength1 = float(line.split()[0])
			writefile.append(line)
		elif (i-5) % (keytrj+2) == 1 and i > 2 and check == 'ljp':
			r = np.array([float(line.split()[0]),float(line.split()[1]),float(line.split()[2])])
			number += 1
			if r[1] > -sidelength1/4 and r[1] < sidelength1/4:
				if (r[1] > -sidelength1/4 and r[1] < -sidelength1 + buffer_width) or (r[1] > sidelength1/4 - buffer_width and r[1] < sidelength1/4):
					record_i_buffer2.append(i-1)
				record_i.append(i-1)
			elif (r[1] > -sidelength1/4 - buffer_width and r[1] < -sidelength1/4) or (r[1] > sidelength1/4 and r[1] < sidelength1/4 + buffer_width):
				record_i_buffer1.append(i-1)
			writefile.append(line)
		else:
			writefile.append(line)
		check = line.split()[0]

print 'number of particles in the buffer 1:' + str(len(record_i_buffer1)) + '\n'
print 'number of particles in the buffer 2:' + str(len(record_i_buffer2)) + '\n'
print 'number of particles in the middle:' + str(len(record_i)) + '\n'

if len(record_i) < number/2:
	temp = random.sample(record_i_buffer1,number/2 - len(record_i))
	record_i += temp
elif len(record_i) > number/2:
	temp = random.sample(record_i_buffer2,len(record_i) - number/2)
	record_i = [item for item in record_i if item not in temp]
elif len(record_i) == number/2:
	pass


record_i_2 = copy.deepcopy(record_i)
for i in record_i:
	for j in range(3):
		record_i_2.append(i+j+1)

ii = 0
index = 1
with open(filename_to,'w') as f:
	for i in range(len(writefile)):
		line = writefile[i]
		if i in range(5):
			f.write(line)
		elif i in record_i:
			f.write('wcap'+'               '+str(index)+'\n')
			mark = True
			ii = i
			index += 1
		elif mark and (i == ii + 1 or i == ii + 2 or i == ii + 3):
			f.write(line)
	for i in range(len(writefile)):
		line = writefile[i]
		if i not in record_i_2 and i not in range(5):
			if line.split()[0] == 'ljp':
				f.write(line.split()[0]+'               '+str(index)+'\n')
				index += 1
			else:
				f.write(line)