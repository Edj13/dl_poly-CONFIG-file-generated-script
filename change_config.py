import numpy as np
from math import *
import sys

filename = sys.argv[1]
writefile = []
count = 0

with open(filename,'r') as f:
	for i,line in enumerate(f):
		if i == 1:
			keytrj = int(line.split()[0])

with open(filename,'r') as f:
	for i, line in enumerate(f):
		if i == 1:
			writefile.append(line)
		elif i == 2:
			sidelength = float(line.split()[0])
			writefile.append(line)
		elif (i-5) % (keytrj+2) == 1 and i > 2:
			count = count + 1
			r = np.array([float(line.split()[0]),float(line.split()[1]),float(line.split()[2])])
			if count == 1:
				writefile.append(line)
				r0 = r
			elif count == 2:
				delta_r = np.abs(r0 - r)
				if delta_r[2] >= sidelength/2.0:
					if r[2] < 0:
						r[2] = r[2] + sidelength
					elif r[2] > 0:
						r[2] = r[2] - sidelength
				writefile.append(("%.12f" % r[0]).rjust(20)+("%.12f" % r[1]).rjust(20)+("%.12f" % r[2]).rjust(20)+'\n')
			elif count == 3:
				delta_r = np.abs(r0 - r)
				if delta_r[2] >= sidelength/2.0:
					if r[2] < 0:
						r[2] = r[2] + sidelength
					elif r[2] > 0:
						r[2] = r[2] - sidelength
				writefile.append(("%.12f" % r[0]).rjust(20)+("%.12f" % r[1]).rjust(20)+("%.12f" % r[2]).rjust(20)+'\n')	
				count = 0
		else:
			writefile.append(line)

with open('CONFIG.temp','w') as f:
	for line in writefile:
		f.write(line)