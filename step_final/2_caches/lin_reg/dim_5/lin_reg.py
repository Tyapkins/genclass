import json
import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures


from matplotlib.pyplot import figure

patt = re.compile(r"\'.*\'")
Xs = []
Ys = []
known_dots, values = [], []

with open('./new_res.txt', 'r') as res:
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

model.fit(new_Xs,Ys)

print(model.coef_)
pred_values, pred_Ys, pred_dots = [], [], []

with open('./new_true.txt', 'r') as res:
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
pred = open('../prediction.txt', 'w')
pred.write('P : T\n\n\n')
res = []
for i, num in enumerate(pred_Ys):
    pred.write(str(int(num>0))+' : ' + str(pred_values[i]) + '\n')
    res.append(int(num>0))
#print(res)
count = 0
for i in range(len(res)):
    #print("{a} : {b}".format(a=res[i], b=pred_values[i]))
    if (res[i] == pred_values[i]):
        count += 1
print(count)
pred.write("\n\n RES:  " + str(count))
pred.close()
