import json
import re
import sys
from random import choice
from collections import Counter
import numpy as np
from ivis import Ivis
from sklearn.preprocessing import MinMaxScaler
from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.pyplot import figure


patt = re.compile(r"\'.*\'")
known_dots, values = [], []
with open('new_final.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        # print(b)
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        num = (b[-1]).replace(' ', '')
        if not(((dot[0] <= 0.26) or (dot[0] >= 0.272))
        or ((dot[1] <= 0.26) or (dot[1] >= 0.272))
        or ((dot[2] <= 0.26) or (dot[2] >= 0.272))):
            known_dots.append(np.array(dot))
            values.append(int(num))
        else:
            print(line)
#to_del = []
#for j in range(len(known_dots)):
#    if (((known_dots[j][0] <= 0.26) or (known_dots[j][0] >= 0.272))
#    or ((known_dots[j][1] <= 0.26) or (known_dots[j][1] >= 0.272))
#    or ((known_dots[j][2] <= 0.26) or (known_dots[j][2] >= 0.272))):
#        to_del.append(j)
        #known_dots.pop(j)
        #exit(0)
#iris = datasets.load_iris()
#X = iris.data


X=np.array(known_dots)
#X_scaled = MinMaxScaler().fit_transform(X)
#print(len(known_dots), len(values))
#exit()

model = Ivis(embedding_dims=2, k=15)

embeddings = model.fit_transform(X)


#first_x, second_y = [], []
#for emb in embeddings:
#    first_x.append(emb[0])
#    second_y.append(emb[1])

#print(first_x)
#print(second_y)

#print(embeddings)
ones=[]
zeros=[]
twos = []
for i in range(len(values)):
    if values[i]==0:
        zeros.append(embeddings[i])
    elif values[i]==1:
        ones.append(embeddings[i])
    else:
        twos.append(embeddings[i])
        
figure(figsize=(12, 9), dpi=120)
plt.plot(list(zip(*ones))[0], list(zip(*ones))[1], 'ro')
plt.plot(list(zip(*zeros))[0], list(zip(*zeros))[1], 'bo')
plt.plot(list(zip(*twos))[0], list(zip(*twos))[1], 'go')
#plt.figure(figsize=(30,20))
#plt.axis([0, 6, 0, 20])
plt.show()



old_values = []
with open('old_final.txt', 'r') as old_res:
    for line in old_res:
        b = line.split(";")
        num = (b[-1]).replace(' ', '')
        old_values.append(int(num))
#print(old_values)

#old_X=np.array(known_dots)

#model = Ivis(embedding_dims=2, k=15)

#mbeddings = model.fit_transform(X)

exit(0)
old_ones=[]
old_zeros=[]
for i in range(len(values)):
    if old_values[i]==0:
        old_zeros.append(embeddings[i])
    else:
        old_ones.append(embeddings[i])
        
figure(figsize=(12, 9), dpi=80)
plt.plot(list(zip(*old_ones))[0], list(zip(*old_ones))[1], 'ro')
plt.plot(list(zip(*old_zeros))[0], list(zip(*old_zeros))[1], 'bo')
#plt.figure(figsize=(30,20))
#plt.axis([0, 6, 0, 20])
plt.show()
