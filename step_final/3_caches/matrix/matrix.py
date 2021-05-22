from numpy import array, zeros, diag
from scipy.linalg import lu, qr, cholesky, svd, schur
import numpy as np
import matplotlib.pyplot as plt

matrix = []
vals = []
with open('full_table.txt', 'r') as res:
    for line in res:

        b = line.split(";")
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        num = (b[-1]).replace(' ', '')
        if not (((dot[0] <= 0.26) or (dot[0] >= 0.272))
        or ((dot[1] <= 0.26) or (dot[1] >= 0.272))):
            vals.append(int(num))
            matrix.append(dot)
MATRIX = array(matrix)

def do_QR(matr):
    Q, R = qr(matr, 2)
    print(Q)
    print(R)
    #reconstruct
    B = Q.dot(R)
    print(B)
    return (Q,R)

def do_LU(matr):
    P, L, U = lu(matr)
    print(P)
    print(L)
    print(U)
    # reconstruct
    B = P.dot(L).dot(U)
    print(B)
    return(P, L, U)

def do_SVD(matr):
    U, s, VT = svd(matr)
    Sigma = zeros((MATRIX.shape[0], MATRIX.shape[1]))
    # populate Sigma with n x n diagonal matrix
    Sigma[:MATRIX.shape[1], :MATRIX.shape[1]] = diag(s)
    return (U, Sigma, VT)

def do_cholesky(matr):
    # useless in our case
    L = cholesky(matr)
    print(L)
    #reconstruct
    B = L.dot(L.T)
    print(B)
    return L

dim = 1
mas_dim = [j for j in range(dim)]
mas = do_SVD(MATRIX)

first_mat = mas[0][np.ix_([i for i in range(len(mas[0]))],mas_dim)]
second_mat = mas[1][np.ix_(mas_dim,mas_dim)]
third_mat = mas[2][np.ix_(mas_dim,[i for i in range(len(mas[2][0]))])]

with open(str(dim)+'_dim_fin.txt', 'w') as mat:
    for line in first_mat:
        mat.write(str(line)+'\n')
    mat.write('\n\n\n')
    mat.write(str(second_mat) + '\n\n')
    mat.write(str(third_mat) + '\n\n')
final_mat = first_mat.dot(second_mat.dot(third_mat))
count = 0
new_count = 0
check = []
print(np.sum(abs(final_mat-MATRIX)))
with open('final.txt', 'w') as f:
    for i, line in enumerate(final_mat):
        f.write("{a} : {b}\n".format(a=MATRIX[i], b=line))
        sub_count = 0
        for j, num in enumerate(MATRIX[i]):
            #print(num, line[j])
            if (abs(num-line[j]) < 1.0e-04):
                sub_count += 1
        if (sub_count == 3):
            count += 1

        arr = [MATRIX[i][0], MATRIX[i][1], MATRIX[i][2]]
        new_arr = [line[0], line[1], line[2]]

        arr_ind = arr.index(max(arr))
        new_ind = new_arr.index(max(new_arr))
        check.append(new_ind)
        if (arr_ind == new_ind):
            new_count += 1
reds, blues, greens = [], [], []
for i in range(len(vals)):
    if (vals[i] == 0):
        blues.append(-first_mat[i])
    elif (vals[i] == 1):
        reds.append(-first_mat[i])
    else:
        greens.append(-first_mat[i])
plt.plot(greens, [1]*len(greens), 'go')
plt.plot(reds, [1]*len(reds), 'ro')
plt.plot(blues, [1]*len(blues), 'bo')
plt.show()