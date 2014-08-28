import numpy as np
from math import *
import sys
import copy

filename = sys.argv[1]
filename_to = sys.argv[2]
writefile = []
record_i = []
check = 'False'
mark = False

with open(filename,'r') as f:
	for i,line in enumerate(f):
		if i == 1:
			keytrj = int(line.split()[0])

with open(filename,'r') as f:
	for i, line in enumerate(f):
		if i == 2:
			sidelength1 = float(line.split()[0])
			writefile.append(line)
		elif (i-5) % (keytrj+2) == 1 and i > 2 and check == 'OW':
			r = np.array([float(line.split()[0]),float(line.split()[1]),float(line.split()[2])])
			if r[1] > -sidelength1/4 and r[1] < sidelength1/4:
				record_i.append(i-1)
			writefile.append(line)
		else:
			writefile.append(line)
		check = line.split()[0]

record_i_2 = copy.deepcopy(record_i)
for i in record_i:
	for j in range(11):
		record_i_2.append(i+j+1)

ii = 0
index = 1
with open(filename_to,'w') as f:
	for i in range(len(writefile)):
		line = writefile[i]
		if i in range(5):
			f.write(line)
		elif i in record_i:
			f.write('OG'+'               '+str(index)+'\n')
			mark = True
			ii = i
			index += 1
		elif mark and (i == ii + 1 or i == ii + 2 or i == ii + 3):
			f.write(line)
		elif mark and i == ii + 4:
			f.write('HG'+'               '+str(index)+'\n')
			index += 1
		elif mark and (i == ii + 5 or i == ii + 6 or i == ii + 7):
			f.write(line)
		elif mark and i == ii + 8:
			f.write('HG'+'               '+str(index)+'\n')
			index += 1
		elif mark and (i == ii + 9 or i == ii + 10):
			f.write(line)
		elif mark and i == ii + 11:
			f.write(line)
			mark = False
	for i in range(len(writefile)):
		line = writefile[i]
		if i not in record_i_2 and i not in range(5):
			if line.split()[0] == 'OW' or line.split()[0] == 'HW':
				f.write(line.split()[0]+'               '+str(index)+'\n')
				index += 1
			else:
				f.write(line)

print len(record_i)