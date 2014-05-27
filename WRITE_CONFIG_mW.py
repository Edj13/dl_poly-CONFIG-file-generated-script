from math import *

# create and open CONFIG file
fout = open("CONFIG","w")

# write the header
fout.write("mW water Shi 2014.04.30\n")

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

# write the coordinates of mW water coarse-grained site
# initially each water site is located on the lattice points

l = 10.0       # total number of particles is 1000. 1000**(1/3)=16
small_D = D/l  # sidelength of a small cell
N = 1000       # number of particles in the box

for n in range(1,N+1):
    fout.write("water".ljust(8)+str(n).rjust(10)+"\n")
    k = ceil((float(n)/(int(l)**2)))
    temp = n-(k-1)*int(l)**2
    j = ceil(temp/l)
    i = temp - (j-1)*l
    x = (i-1)*small_D + (-D/2.0 + small_D/2.0)
    y = -(j-1)*small_D + (D/2.0 - small_D/2.0)
    z = -(k-1)*small_D + (D/2.0 - small_D/2.0)
    fout.write(("%.12f" % x).rjust(20)+("%.12f" % y).rjust(20)+("%.12f" % z).rjust(20)+"\n")
    # assign the zero initial velocities to each particles
    # fout.write(("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+("%.12f" % 0.00).rjust(20)+"\n")

fout.close()