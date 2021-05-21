from numpy import array, zeros, diag
from scipy.linalg import lu, qr, cholesky, svd, schur
from sklearn.decomposition import PCA
import random
import numpy as np
import matplotlib.pyplot as plt
from implicit import als
from scipy.sparse import coo_matrix

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
    #print(U)
    #print(s)
    #print(VT)
    Sigma = zeros((MATRIX.shape[0], MATRIX.shape[1]))
    # populate Sigma with n x n diagonal matrix
    Sigma[:MATRIX.shape[1], :MATRIX.shape[1]] = diag(s)
    #B = U.dot(Sigma.dot(VT))
    #print(B)
    return (U, Sigma, VT)

def do_cholesky(matr):
    # useless in our case
    L = cholesky(matr)
    print(L)
    #reconstruct
    B = L.dot(L.T)
    print(B)
    return L

#new_matrix = MATRIX
#new_matrix = np.insert(new_matrix, [0], ['1.0', '2.0', '3.0'])
#print(new_matrix)
#import pandas as pd
#data = pd.read_csv('matrix.csv')
#print(data.head())
#print(data.isnull().sum())
#exit(0)

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
#MATRIX = MATRIX[0][0]
#new_matrix = coo_matrix(MATRIX)
#new_matrix[0][0] = 0
copy_matrix = MATRIX.copy()

NUM = 1000
#test_matrix = coo_matrix(copy_matrix[:NUM])
test_matrix = copy_matrix[:NUM]
new_matrix = copy_matrix[NUM+1:2*NUM+1]

mas = do_SVD(test_matrix)

dim = 1
mas_dim = [j for j in range(dim)]

first_known = mas[0]
second_known = mas[1]
third_known = mas[2]

first_mat = mas[0][np.ix_([i for i in range(len(mas[0]))],mas_dim)]
second_mat = mas[1][np.ix_(mas_dim,mas_dim)]
third_mat = mas[2][np.ix_(mas_dim,[i for i in range(len(mas[2][0]))])]

#print(second_mat, third_mat)
rec_mat = first_mat.dot(second_mat.dot(third_mat))
print(np.sum(abs(rec_mat-test_matrix)))


#exit()

#new_matrix = copy_matrix[NUM+1:2*NUM+1]
#save_matrix = new_matrix.copy()
#aver = new_matrix.mean(0)
#new_matrix = np.transpose(new_matrix)
#test_matrix = np.transpose(test_matrix)
#print(aver)
#exit(0)
#try_mat = coo_matrix(copy_matrix[:2*NUM])

#list_del = []
#N = 50
#pair = (-1, -1)
#for i in range(N):
#    while pair[0] in list_del:
#        if (-1) not in list_del:
#            list_del.append(-1)
#        pair = (random.randint(0, len(new_matrix)-1), random.randint(0,2))
#    list_del.append(pair[0])
#    new_matrix[pair[0]][pair[1]] = 0

#for j in range(len(MATRIX)):
#    print(0)

#als_model = als.AlternatingLeastSquares()
#new_mat = als_model.fit(try_mat)

#exit(0)

#print(als_model.item_norms)
#for i in range(5):
#    a = als_model.similar_items(i)
#    print(a)
#print(als_model.recommend_all(new_matrix, N=3))

#exit(0)
dim = 1
mas_dim = [j for j in range(dim)]
mas = do_SVD(MATRIX)

first_mat = mas[0][np.ix_([i for i in range(len(mas[0]))],mas_dim)]
second_mat = mas[1][np.ix_(mas_dim,mas_dim)]
third_mat = mas[2][np.ix_(mas_dim,[i for i in range(len(mas[2][0]))])]

#print(first_mat)
#print(second_mat)
#print(third_mat)
with open('1_dim_fin.txt', 'w') as mat:
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
        print(arr[arr_ind], new_arr[new_ind])
        print(arr_ind, new_ind)
        check.append(new_ind)
        if (arr_ind == new_ind):
            new_count += 1
print(count)
print(new_count)
print(check)
reds, blues, greens = [], [], []
for i in range(len(vals)):
    if (vals[i] == 0):
        blues.append(-first_mat[i])
    elif (vals[i] == 1):
        reds.append(-first_mat[i])
    else:
        greens.append(-first_mat[i])
print(len(reds), len(blues), len(greens))
plt.plot(greens, [1]*len(greens), 'go')
plt.plot(reds, [1]*len(reds), 'ro')
plt.plot(blues, [1]*len(blues), 'bo')
plt.show()
#print(final_mat)