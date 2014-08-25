from math import *
import numpy as np
from time import strftime
import sys

with open('ConfigSymInfo','r') as f:
    for i, line in enumerate(f):
        if i == 0:
            contr_header = line
        # LX,LY,LZ are the dimension of simulation box
        # lx,ly,lz are the dimension of actuall space you want the particles distributed in
        if line.split()[0] == 'VX':
            VX = np.array([float(line.split()[1]),float(line.split()[2]),float(line.split()[3])])
        elif line.split()[0] == 'VY':
            VY = np.array([float(line.split()[1]),float(line.split()[2]),float(line.split()[3])])
        elif line.split()[0] == 'VZ':
            VZ = np.array([float(line.split()[1]),float(line.split()[2]),float(line.split()[3])])
        elif line.split()[0] == 'vx':
            vx = np.array([float(line.split()[1]),float(line.split()[2]),float(line.split()[3])])
        elif line.split()[0] == 'vy':
            vy = np.array([float(line.split()[1]),float(line.split()[2]),float(line.split()[3])])
        elif line.split()[0] == 'vz':
            vz = np.array([float(line.split()[1]),float(line.split()[2]),float(line.split()[3])])
        elif line.split()[0] == 'levcfg':
            levcfg = int(line.split()[1])      # see below
        elif line.split()[0] == 'imcon':
            imcon = int(line.split()[1])       # see below
        elif line.split()[0] == 'nmolecules':
            N = int(line.split()[1])           # number of molecules in the box
        elif line.split()[0] == 'I1':
            I1 = float(line.split()[1])        # declare the value of I1. Refer to Water Model


if len(sys.argv) != 2:
    print "Arguments should be: output file"
    sys.exit()
else:
    filedirectory_to = sys.argv[1]

# create a rotation matrix
def rotateMatrix(theta,beta,gamma):
    rx = [[1,0,0],[0,cos(theta),-sin(theta)],[0,sin(theta),cos(theta)]]
    ry = [[cos(beta),0,sin(beta)],[0,1,0],[-sin(beta),0,cos(beta)]]
    rz = [[cos(gamma),-sin(gamma),0],[sin(gamma),cos(gamma),0],[0,0,1]]
    return np.dot(np.dot(rx,ry),rz)

# create and open CONFIG file
fout = open(filedirectory_to,"w")

# write the header
fout.write(contr_header.rstrip()+' I1='+str(I1)+'  '+strftime("%Y-%m-%d %H:%H:%S")+'\n')

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
fout.write(str(levcfg).rjust(10)+str(imcon).rjust(10)+"\n")

# write the simulation box cell vector
fout.write(format(VX[0],'.12f').rjust(20)+format(VX[1],'.12f').rjust(20)+format(VX[2],'.12f').rjust(20)+"\n")
fout.write(format(VY[0],'.12f').rjust(20)+format(VY[1],'.12f').rjust(20)+format(VY[2],'.12f').rjust(20)+"\n")
fout.write(format(VZ[0],'.12f').rjust(20)+format(VZ[1],'.12f').rjust(20)+format(VZ[2],'.12f').rjust(20)+"\n")

# write the coordinates of SPC/E water atoms
# initially put all atoms approximately at the lattice points

lx = sqrt(vx[0]**2+vx[1]**2+vx[2]**2)
ly = sqrt(vy[0]**2+vy[1]**2+vy[2]**2)
lz = sqrt(vz[0]**2+vz[1]**2+vz[2]**2)

small_D = (lx*ly*lz/float(N))**(1./3.)         # sidelength of a small cell. each such cell contains one molecule

nx = int(ceil(lx/small_D))
ny = int(ceil(ly/small_D))
nz = int(ceil(lz/small_D))

natm = 5

# mole_struchedral water stucture

mole_struc0 = np.array([[0,0,I1],[-2*sqrt(2)*I1/3.,0,-I1/3.],[sqrt(2)*I1/3.,-sqrt(6)*I1/3.,-I1/3.],[sqrt(2)*I1/3.,sqrt(6)*I1/3.,-I1/3]])

for n in range(1,N+1):
    fout.write("OW".ljust(8)+str((n-1)*natm+1).rjust(10)+"\n")    # write the coordinate of oxygen atom
    k = int(ceil(float(n)/(nx*ny)))
    temp = n-(k-1)*(nx*ny)
    j = ceil(float(temp)/ny)
    i = temp - (j-1)*ny
    x = -(j-1)*(lx/nx) + (lx/2.0 - (lx/nx)/2.0)
    y = (i-1)*(ly/ny) + (-ly/2.0 + (ly/ny)/2.0)
    z = -(k-1)*(lz/nz) + (lz/2.0 - (lz/nz)/2.0)
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