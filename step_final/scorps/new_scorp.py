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
known_dots, values = [], []

with open('res1-1000.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        num = (b[-1]).replace(' ', '')
        val = (b[-2]).replace(' ', '')
        values.append(int(num))
        Ys.append(float(val))
        a = patt.search(line)
        mas = a[0].split(", ")
        new_mas = [int(a[1:-2]) for a in mas]
        known_dots.append(new_mas)
#print(known_dots)
#print(Ys)
model = LinearRegression(normalize=True)
new_Xs = np.array(known_dots)
#normalized_X = preprocessing.normalize(new_Xs)
#standardized_X = preprocessing.scale(normalized_X)
plt.figure(figsize=(20,10))

#print(new_Xs)

model.fit([[t[i] for i in range(5)] for t in new_Xs],
        [t for t in Ys], )

print(model.coef_)
pred_values, pred_Ys, pred_dots = [], [], []

with open('res1001-2000.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        num = (b[-1]).replace(' ', '')
        val = (b[-2]).replace(' ', '')
        pred_values.append(int(num))
        pred_Ys.append(float(val))
        a = patt.search(line)
        mas = a[0].split(", ")
        new_mas = [int(a[1:-2]) for a in mas]
        pred_dots.append(new_mas)

pred_Xs = np.array(pred_dots)
pred_Ys = model.predict(pred_Xs)
#print(pred_Ys)
res = []
for i in pred_Ys:
    res.append(int(i>0))
print(res)
count = 0
for i in range(len(res)):
    print("{a} : {b}".format(a=res[i], b=pred_values[i]))
    if (res[i] == pred_values[i]):
        count += 1
print(count)
