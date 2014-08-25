from math import *
import numpy as np
import sys
from time import strftime

if len(sys.argv) != 4:
    print "Arguments should be: sidelength, # of molecules and I1 and output file"
    sys.exit()
else:
    D = float(sys.argv[1])         # sidelength of simulation cubic box
    N = sys.argv[2]                # number of particles in the box
    if float(N) == int(N):
        N = int(N)
    else:
        print "the number of molecules must be an integer"
        sys.exit()
    filedirectory_to = sys.argv[3]

# create and open CONFIG file
fout = open(filedirectory_to,"w")

# write the header
fout.write('Configurations for SPCE water model '+strftime("%Y-%m-%d %H:%H:%S")+'\n')

# write the levcfg and imcon key
# levcfg: 0 Coordinates included in file
#         1 Coordinates and velocities included in file
#         2 Coordinates, velocities and forces included in file
# imcon:  0 no periodic boundaries
#         1 cubic boundary conditions
#         2 orthorhombic boundary conditions
#         3 parallelepiped boundary conditions
#         4 truncated octahedral boundary conditions
#         5 rhombic dodecahedral boundary conditions
#         6 x-y parallelogram boundary conditions with no periodicity in the z direction
#         7 hexagonal prism boundary conditions
fout.write(str(0).rjust(10)+str(2).rjust(10)+"\n")

# write the simulation box cell vector
fout.write((str(D)+"000000000000").rjust(20)+("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")
fout.write(("%.12f" % 0.00).rjust(20)+(str(D)+"000000000000").rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")
fout.write(("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+(str(D)+"000000000000").rjust(20)+"\n")

# write the coordinates of SPC/E water atoms
# initially put all atoms approximately at the lattice points

l = ceil(N**(1./3.))       # total number of particles is 1000. 1000**(1/3)=10
small_D = D/l              # sidelength of a small cell
natm = 3

for n in range(1,N+1):
    fout.write("OW".ljust(8)+str((n-1)*natm+1).rjust(10)+"\n")    # write the coordinate of oxygen atom
    k = ceil((float(n)/(int(l)**2)))
    temp = n-(k-1)*int(l)**2
    j = ceil(temp/l)
    i = temp - (j-1)*l
    x = -(j-1)*small_D + (D/2.0 - small_D/2.0)
    y = (i-1)*small_D + (-D/2.0 + small_D/2.0)
    z = -(k-1)*small_D + (D/2.0 - small_D/2.0)
    fout.write(("%.12f" % x).rjust(20)+("%.12f" % y).rjust(20)+("%.12f" % z).rjust(20)+"\n")
    # assign the zero initial velocities to each particles
    #fout.write(("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")

    phi1 = 2*pi*np.random.random()
    phi2 = 2*pi*np.random.random()
    theta1 = pi*np.random.random()
    theta2 = (109.47/180)*pi         # the HOH angle is 109.47 degree

    x1 = sin(theta1)*cos(phi1)
    y1 = sin(theta1)*sin(phi1)
    z1 = cos(theta1)
    x2 = sin(phi1)*cos(phi2)*sin(theta2)+cos(theta1)*cos(phi1)*sin(phi2)*sin(theta2)+sin(theta1)*cos(phi1)*cos(theta2)
    y2 = -cos(phi1)*cos(phi2)*sin(theta2)+cos(theta1)*sin(phi1)*sin(phi2)*sin(theta2)+sin(theta1)*sin(phi1)*cos(theta2)
    z2 = -sin(theta1)*sin(phi2)*sin(theta2)+cos(theta1)*cos(theta2)

    # randomly put the Hydrogen atoms in the unit cell while keeping the structure right
    fout.write("HW".ljust(8)+str((n-1)*natm+2).rjust(10)+"\n")    # write the coordinate of hydrogen atom
    fout.write(("%.12f" % (x1+x)).rjust(20)+("%.12f" % (y1+y)).rjust(20)+("%.12f" % (z1+z)).rjust(20)+"\n")

    fout.write("HW".ljust(8)+str((n-1)*natm+3).rjust(10)+"\n")
    fout.write(("%.12f" % (x2+x)).rjust(20)+("%.12f" % (y2+y)).rjust(20)+("%.12f" % (z2+z)).rjust(20)+"\n")

fout.close()