import scipy.linalg
from numpy import array
from scipy.linalg import lu, qr, cholesky, svd
# define a square matrix
matrix = []
values = []
with open('full_table.txt', 'r') as res:
    for line in res:

        b = line.split(";")
        # print(b)
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        num = (b[-1]).replace(' ', '')
        #print(dot)
        if not (((dot[0] <= 0.26) or (dot[0] >= 0.272))
        or ((dot[1] <= 0.26) or (dot[1] >= 0.272))):
                matrix.append(dot)
                values.append(int(num))
MATRIX = array(matrix)


from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

import numpy as np
greens = []
reds = []
blues = []
for i, dot in enumerate(MATRIX):
    #print(i, dot)
    if (values[i] == 2):
        greens.append(dot)
    elif (values[i] == 1):
        reds.append(dot)
    else:
        blues.append(dot)
greens = np.array(greens)
reds = np.array(reds)
blues = np.array(blues)

tri = Delaunay(MATRIX).convex_hull
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(greens[:,0], greens[:,1], greens[:,2], zdir='y', color='g')
ax.scatter(reds[:,0], reds[:,1], reds[:,2], zdir='y', color='r')
ax.scatter(blues[:,0], blues[:,1], blues[:,2], zdir='y', color='b')
xs = [i[0] for i in MATRIX]
ys = [i[1] for i in MATRIX]
zs = [i[2] for i in MATRIX]
ax.set_xlim3d(min(xs), max(xs))
ax.set_ylim3d(min(ys), max(ys))
ax.set_zlim3d(min(zs), max(zs))

plt.show()
