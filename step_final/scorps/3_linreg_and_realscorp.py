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
from sklearn.linear_model import LinearRegression
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA


from matplotlib.pyplot import figure

patt = re.compile(r".*")
dots = []
Xs = []
Ys = []
values = []        

with open('new_final.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        #print(b)
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        num = (b[-1]).replace(' ', '')
        if not (((dot[0] <= 0.26) or (dot[0] >= 0.272))
        or ((dot[1] <= 0.26) or (dot[1] >= 0.272))
        or ((dot[2] <= 0.26) or (dot[2] >= 0.272))):
            dots.append(np.array(dot))
            values.append(int(num))
#print(dots)
scorp = PCA(n_components=2)
scorp.fit(dots)
X_2D = scorp.transform(dots)
print(X_2D)
for i in X_2D:
    Xs.append(i[0])
    Ys.append(i[1])
plt.figure(figsize=(20,10))
x = np.array(Xs)
y = np.array(Ys)

model = LinearRegression(fit_intercept=True)

model.fit(x[:, np.newaxis], y)

print(model.coef_)
xfit = np.linspace(-0.01, 0.01, 1000)
yfit = model.predict(xfit[:, np.newaxis])

#plt.scatter(x, y)
plt.plot(xfit, yfit, 'yo', linewidth=1)

for i in range(len(Xs)):
    if (values[i] == 1):
        plt.plot(Xs[i], Ys[i], 'ro')
    elif (values[i] == 0):
        plt.plot(Xs[i], Ys[i], 'bo')
    else:
        plt.plot(Xs[i], Ys[i], 'go')

plt.show()

#model.fit(x[:, np.newaxis], y)

#xfit = np.linspace(0, 10, 1000)
#yfit = model.predict(xfit[:, np.newaxis])

#plt.scatter(x, y)
#plt.plot(xfit, yfit)

#plt.show()
#exit(0)


#old_X=np.array(known_dots)

#model = Ivis(embedding_dims=2, k=15)

#mbeddings = model.fit_transform(X)


#old_ones=[]
#old_zeros=[]
#old_values = []
#embeddings = []
#for i in range(len(values)):
#    if old_values[i]==0:
#        old_zeros.append(embeddings[i])
#    else:
#        old_ones.append(embeddings[i])
        
#figure(figsize=(12, 9), dpi=80)
#plt.plot(list(zip(*old_ones))[0], list(zip(*old_ones))[1], 'ro')
#plt.plot(list(zip(*old_zeros))[0], list(zip(*old_zeros))[1], 'bo')
#plt.figure(figsize=(30,20))
#plt.axis([0, 6, 0, 20])
#plt.show()
