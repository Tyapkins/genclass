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
from sklearn import preprocessing
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score


from matplotlib.pyplot import figure

patt = re.compile(r"\'.*\'")
Xs = []
Ys = []
all_dots, known_dots, values = [], [], []
pred_values, pred_Ys, pred_dots = [], [], []

with open('new_final.txt', 'r') as res:
    for i, line in enumerate(res):
        b = line.split(";")
        num = (b[-1]).replace(' ', '')
        val = (b[-2]).replace(' ', '')
        values.append(int(num))
        Ys.append(float(val))
        a = patt.search(line)
        mas = a[0].split(", ")
        new_mas = [int(a[1:-2]) for a in mas]
        all_dots.append(new_mas)
        if (i != 69):
            if (i <= 1000):
                known_dots.append(new_mas)
            elif (i <= 1100):
                pred_dots.append(new_mas)
        else:
            print(i)
            print(line)

#print(known_dots)
#print(Ys)
#model = LinearRegression(normalize=True)
new_Xs = np.array(all_dots)
#normalized_X = preprocessing.normalize(new_Xs)
#standardized_X = preprocessing.scale(normalized_X)
plt.figure(figsize=(20,10))

#print(new_Xs)

iv_model = Ivis(embedding_dims=2, k=15)

embeddings = iv_model.fit_transform(new_Xs)

print(len(embeddings))
x = []
y = []
pred_x, pred_y = [], []
for i in range(len(embeddings)):
    if (i <= 1000):
        x.append(embeddings[i][0])
        y.append(embeddings[i][1])
    elif (i <= 1100):
        pred_x.append(embeddings[i][0])
        pred_y.append(embeddings[i][1])
x = np.array(x)
y = np.array(y)
model = LinearRegression(fit_intercept=True)

model.fit(x[:, np.newaxis], y)

print(model.coef_)

for i in range(len(x)):
    if (values[i] == 0):
        plt.plot(x[i], y[i], 'ro')
    elif (values[i] == 1):
        plt.plot(x[i], y[i], 'bo')


pred_Xs = np.array(pred_x)
pred_Ys = model.predict(pred_Xs.reshape(-1,1))
for i in range(len(pred_Xs)):
    plt.plot(pred_Xs[i], pred_Ys[i], 'go')
plt.show()
#print(pred_Ys)
#res = []
#for i in pred_Ys:
#    res.append(int(i>0))
#print(res)
#count = 0
#for i in range(len(res)):
#    print("{a} : {b}".format(a=res[i], b=pred_values[i]))
#    if (res[i] == pred_values[i]):
#        count += 1
#print(count)
