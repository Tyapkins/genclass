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


from matplotlib.pyplot import figure

patt = re.compile(r".*")
dots = []
Xs = []
Ys = []
values = []        

with open('old_final.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        #print(b)
        dot = b[2:4]
        dot[0] = float(dot[0].replace(' ', ''))
        dot[1] = float(dot[1].replace(' ', ''))
        num = (b[-1])[1:-2]
        #print(dot)
        #print(num)
        dots.append(dot)
        if (float(dot[1]) > 0.22):
            Xs.append(dot[0])
            Ys.append(dot[1])
            values.append(int(num))

plt.figure(figsize=(20,10))
x = np.array(Xs)
y = np.array(Ys)

model = LinearRegression(fit_intercept=True)

model.fit(x[:, np.newaxis], y)

print(model.coef_)
xfit = np.linspace(0.26, 0.275, 1000)
yfit = model.predict(xfit[:, np.newaxis])

#plt.scatter(x, y)
plt.plot(xfit, yfit, 'go', linewidth=1)

for i in range(len(Xs)):
    if (values[i] == 1):
        plt.plot(Xs[i], Ys[i], 'ro')
    else:
        plt.plot(Xs[i], Ys[i], 'bo')

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
