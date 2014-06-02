from math import *
import numpy as np

# create a rotation matrix 123
def rotateMatrix(theta,beta,gamma):
    rx = [[1,0,0],[0,cos(theta),-sin(theta)],[0,sin(theta),cos(theta)]]
    ry = [[cos(beta),0,sin(beta)],[0,1,0],[-sin(beta),0,cos(beta)]]
    rz = [[cos(gamma),-sin(gamma),0],[sin(gamma),cos(gamma),0],[0,0,1]]
    return np.dot(np.dot(rx,ry),rz)

# create and open CONFIG file
fout = open("CONFIG","w")

# write the header
fout.write("NVT simulation of TIP5P water model Shi 2014.05.30\n")

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
D = 32.5  # sidelength of simulation cubic box
fout.write((str(D)+"000000000000").rjust(20)+("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")
fout.write(("%.12f" % 0.00).rjust(20)+(str(D)+"000000000000").rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")
fout.write(("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+(str(D)+"000000000000").rjust(20)+"\n")

# write the coordinates of SPC/E water atoms
# initially put all atoms approximately at the lattice points

l = 10.0       # total number of particles is 1000. 1000**(1/3)=10
small_D = D/l  # sidelength of a small cell
N = 1000       # number of particles in the boxs
I1 = 0.9572
I2 = 0.7000

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

    r1 = np.array([0,I1*cos(104.52*pi/360),I1*sin(104.52*pi/360)])
    r2 = np.array([0,I1*cos(104.52*pi/360),-I1*sin(104.52*pi/360)])
    r3 = np.array([I2*sin(109.47*pi/360),-I2*cos(109.47*pi/360),0])
    r4 = np.array([-I2*sin(109.47*pi/360),-I2*cos(109.47*pi/360),0])

    R = rotateMatrix(phi1,phi2,phi3)
    r1 = np.dot(R,r1)
    r2 = np.dot(R,r2)
    r3 = np.dot(R,r3)
    r4 = np.dot(R,r4)

    # randomly put the atoms in the unit cell while keeping the structure right
    fout.write("HW".ljust(8)+str((n-1)*3+2).rjust(10)+"\n")    # write the coordinate of hydrogen atom
    fout.write(("%.12f" % (r1[0]+x)).rjust(20)+("%.12f" % (r1[1]+y)).rjust(20)+("%.12f" % (r1[2]+z)).rjust(20)+"\n")

    fout.write("HW".ljust(8)+str((n-1)*3+3).rjust(10)+"\n")
    fout.write(("%.12f" % (r2[0]+x)).rjust(20)+("%.12f" % (r2[1]+y)).rjust(20)+("%.12f" % (r2[2]+z)).rjust(20)+"\n")

    fout.write("OEW".ljust(8)+str((n-1)*3+3).rjust(10)+"\n")
    fout.write(("%.12f" % (r3[0]+x)).rjust(20)+("%.12f" % (r3[1]+y)).rjust(20)+("%.12f" % (r3[2]+z)).rjust(20)+"\n")

    fout.write("OEW".ljust(8)+str((n-1)*3+3).rjust(10)+"\n")
    fout.write(("%.12f" % (r4[0]+x)).rjust(20)+("%.12f" % (r4[1]+y)).rjust(20)+("%.12f" % (r4[2]+z)).rjust(20)+"\n")

fout.close()