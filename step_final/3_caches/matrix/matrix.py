from numpy import array, zeros, diag
from scipy.linalg import lu, qr, cholesky, svd, schur
from sklearn.decomposition import PCA
import numpy as np

matrix = []
vals = []
with open('full_table.txt', 'r') as res:
    for line in res:

        b = line.split(";")
        # print(b)
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
    reconstruct
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
    print(U)
    print(s)
    print(VT)
    Sigma = zeros((MATRIX.shape[0], MATRIX.shape[1]))
    # populate Sigma with n x n diagonal matrix
    Sigma[:MATRIX.shape[1], :MATRIX.shape[1]] = diag(s)
    B = U.dot(Sigma.dot(VT))
    print(B)
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

print(first_mat)
print(second_mat)
print(third_mat)
with open('1_dim_fin.txt', 'w') as mat:
    for line in first_mat:
        mat.write(str(line)+'\n')
    mat.write('\n\n\n')
    mat.write(str(second_mat) + '\n\n')
    mat.write(str(third_mat) + '\n\n')
final_mat = mas[0].dot(mas[1].dot(mas[2]))
count = 0
with open('final.txt', 'w') as f:
    for i, line in enumerate(final_mat):
        f.write("{a} : {b}\n".format(a=MATRIX[i], b=line))
        sub_count = 0
        for j, num in enumerate(MATRIX[i]):
            #print(num, line[j])
            if (abs(num-line[j]) < 1.0e-07):
                sub_count += 1
        if (sub_count == 3):
            count += 1
print(count)
#print(final_mat)