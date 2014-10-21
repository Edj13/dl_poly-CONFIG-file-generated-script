import numpy as np
from math import *
import sys
import copy


filehead = []
atoms = []
with open(sys.argv[1],"r") as f:
	for i, line in enumerate(f):
		if i <= 4:
			if i == 1:
				keytrj = int(line.split()[0])
			filehead.append(line)
		elif i > 4 and (i-5) % (keytrj+2) == 1:
			atoms.append(line)

number_atoms = len(atoms)
random_pick = np.random.choice(int(number_atoms),int(number_atoms)/2,replace=False)
rest_pick = np.setdiff1d(range(int(number_atoms)),random_pick)

with open(sys.argv[2],'w') as f:
	for line in filehead:
		f.write(line)
	for i in range(int(number_atoms)/2):
		f.write("wcap"+'               '+str(i+1)+'\n')
		f.write(atoms[random_pick[i]])
	for i in range(int(number_atoms)/2,int(number_atoms)):
		f.write("ljp"+'               '+str(i+1)+'\n')
		f.write(atoms[rest_pick[i-500]])





