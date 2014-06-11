from math import *
import numpy as np
from time import strftime
import sys

if len(sys.argv) != 5:
    print "Arguments should be: sidelength, # of molecules and I1 and output file"
    sys.exit()
else:
    D = float(sys.argv[1])         # sidelength of simulation cubic box
    N = sys.argv[2]         # number of particles in the box
    if float(N) == int(N):
        N = int(N)
    else:
        print "the number of molecules must be an integer"
        sys.exit()
    I1 = float(sys.argv[3])        # declare the value of I1. Refer to Water Model
    filedirectory_to = sys.argv[4]

# create a rotation matrix
def rotateMatrix(theta,beta,gamma):
    rx = [[1,0,0],[0,cos(theta),-sin(theta)],[0,sin(theta),cos(theta)]]
    ry = [[cos(beta),0,sin(beta)],[0,1,0],[-sin(beta),0,cos(beta)]]
    rz = [[cos(gamma),-sin(gamma),0],[sin(gamma),cos(gamma),0],[0,0,1]]
    return np.dot(np.dot(rx,ry),rz)

# create and open CONFIG file
fout = open(filedirectory_to,"w")

# write the header
fout.write('Configurations for symmetry water model '+'I1='+str(I1)+'  '+strftime("%Y-%m-%d %H:%H:%S")+'\n')

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
natm = 5

# mole_struchedral water stucture

mole_struc0 = np.array([[0,0,I1],[-2*sqrt(2)*I1/3.,0,-I1/3.],[sqrt(2)*I1/3.,-sqrt(6)*I1/3.,-I1/3.],[sqrt(2)*I1/3.,sqrt(6)*I1/3.,-I1/3]])

for n in range(1,N+1):
    fout.write("OW".ljust(8)+str((n-1)*3+1).rjust(10)+"\n")    # write the coordinate of oxygen atom
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
    phi3 = 2*pi*np.random.random()
    # get the rotation matrix
    R = rotateMatrix(phi1,phi2,phi3)

    mole_struc = np.transpose(np.dot(R,np.transpose(mole_struc0)))

    # randomly put the Hydrogen atoms in the unit cell while keeping the structure right
    fout.write("HW".ljust(8)+str((n-1)*natm+2).rjust(10)+"\n")    # write the coordinate of hydrogen atom
    fout.write(("%.12f" % (mole_struc[0][0]+x)).rjust(20)+("%.12f" % (mole_struc[0][1]+y)).rjust(20)+("%.12f" % (mole_struc[0][2]+z)).rjust(20)+"\n")

    fout.write("HW".ljust(8)+str((n-1)*natm+3).rjust(10)+"\n")
    fout.write(("%.12f" % (mole_struc[1][0]+x)).rjust(20)+("%.12f" % (mole_struc[1][1]+y)).rjust(20)+("%.12f" % (mole_struc[1][2]+z)).rjust(20)+"\n")

    fout.write("OEW".ljust(8)+str((n-1)*natm+4).rjust(10)+"\n")
    fout.write(("%.12f" % (mole_struc[2][0]+x)).rjust(20)+("%.12f" % (mole_struc[2][1]+y)).rjust(20)+("%.12f" % (mole_struc[2][2]+z)).rjust(20)+"\n")

    fout.write("OEW".ljust(8)+str((n-1)*natm+5).rjust(10)+"\n")
    fout.write(("%.12f" % (mole_struc[3][0]+x)).rjust(20)+("%.12f" % (mole_struc[3][1]+y)).rjust(20)+("%.12f" % (mole_struc[3][2]+z)).rjust(20)+"\n")

fout.close()