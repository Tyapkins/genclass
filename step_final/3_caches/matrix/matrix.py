from numpy import array, zeros, diag
from scipy.linalg import lu, qr, cholesky, svd, schur
# define a square matrix
matrix = []
with open('full_table.txt', 'r') as res:
    for line in res:

        b = line.split(";")
        # print(b)
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        #num = (b[-1]).replace(' ', '')
        #print(dot)
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
    return (U, s, VT)

def do_cholesky(matr):
    # useless in our case
    L = cholesky(matr)
    print(L)
    reconstruct
    B = L.dot(L.T)
    print(B)
    return L

mas = do_SVD(MATRIX)
print(mas[1])
