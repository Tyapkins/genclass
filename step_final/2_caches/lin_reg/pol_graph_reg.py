import json
import re
import sys
import operator

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
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA



from matplotlib.pyplot import figure

patt = re.compile(r".*")
dots = []
Xs = []
testY, Ys = [], []
values = []

with open('res_table.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        #print(b)
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        num = (b[-1]).replace(' ', '')
        a = b[0].split(', ')
        a = [int("".join([i for i in j if i.isdigit()])) for j in a]
        #new_mas = [i.replace('"', '') for i in a]
        #print(new_mas)
        if not (((dot[0] <= 0.26) or (dot[0] >= 0.272))
        or ((dot[1] <= 0.26) or (dot[1] >= 0.272))):
            dots.append(np.array(a))
            values.append(int(num))
            testY.append(dot[2])
#print(dots)
scorp = PCA(n_components=2)
scorp.fit(dots)
X_2D = scorp.transform(dots)

new_scorp = PCA(n_components=2)
X_3D = []
for i in range(len(X_2D)):
    X_3D.append([X_2D[i][0], X_2D[i][1], testY[i]])
new_scorp.fit(X_3D)
newX_2D = new_scorp.transform(X_3D)
#print(X_2D)
for i in newX_2D:
    Xs.append(i[0])
    Ys.append(i[1])
plt.figure(figsize=(20,10))
x = np.array(Xs)
y = np.array(Ys)

x = x[:, np.newaxis]
y = y[:, np.newaxis]

polynomial_features= PolynomialFeatures(degree=4)
x_poly = polynomial_features.fit_transform(x)

model = LinearRegression()
model.fit(x_poly, y)
y_poly_pred = model.predict(x_poly)

rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
r2 = r2_score(y,y_poly_pred)
print(rmse)
print(r2)

for i in range(len(Xs)):
    if (values[i] == 1):
        plt.plot(Xs[i], Ys[i], 'ro')
    else:
        plt.plot(Xs[i], Ys[i], 'bo')

#plt.scatter(x, y, s=10)
# sort the values of x before line plot
sort_axis = operator.itemgetter(0)
sorted_zip = sorted(zip(x,y_poly_pred), key=sort_axis)
x, y_poly_pred = zip(*sorted_zip)
plt.plot(x, y_poly_pred, color='m')
#plt.show()

#model = make_pipeline(PolynomialFeatures(4), LinearRegression(normalize=True))
#new_Xs = np.array(known_dots)


#plt.figure(figsize=(20,10))

#model.fit(new_Xs,Ys)

#exit(0)

#print(model.coef_)

pred_values, pred_Ys, pred_dots = [], [], []
true_Y = []
#exit(0)

with open('true_table.txt', 'r') as res:
    for line in res:

        b = line.split(";")
        # print(b)
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        num = (b[-1]).replace(' ', '')
        a = b[0].split(', ')
        a = [int("".join([i for i in j if i.isdigit()])) for j in a]
        # new_mas = [i.replace('"', '') for i in a]
        # print(new_mas)
        if not (((dot[0] <= 0.26) or (dot[0] >= 0.272))
        or ((dot[1] <= 0.26) or (dot[1] >= 0.272))):
            pred_dots.append(np.array(a))
            pred_values.append(int(num))
            true_Y.append(dot[2])






#pred_pred_Xs = np.array(pred_dots)
#scorp.fit(pred_pred_Xs)
#pred_Xs = scorp.transform(pred_pred_Xs)

pred_pred_Ys = model.predict(pred_dots)
#print(pred_Ys)

scorp = PCA(n_components=2)
scorp.fit(pred_dots)
pred_X_2D = scorp.transform(pred_dots)
pred_Xs = []
pred_Ys

new_scorp = PCA(n_components=2)
pred_X_3D = []
true_X_3D = []
for i in range(len(pred_X_2D)):
    pred_X_3D.append([pred_X_2D[i][0], pred_X_2D[i][1], pred_pred_Ys[i]])
    true_X_3D.append([pred_X_2D[i][0], pred_X_2D[i][1], true_Y[i]])
new_scorp.fit(pred_X_3D)
pred_newX_2D = new_scorp.transform(pred_X_3D)
#print(X_2D)
for i in pred_newX_2D:
    pred_Xs.append(i[0])
    pred_Ys.append(i[1])
for i in range(len(pred_Xs)):
    if (pred_values[i] == 1):
        plt.plot(pred_Xs[i], pred_Ys[i], 'go')
    else:
        plt.plot(pred_Xs[i], pred_Ys[i], 'yo')
plt.show()
exit()
pred = open('pol_prediction.txt', 'w')
pred.write('P : T\n\n\n')
res = []
for i, num in enumerate(pred_Ys):
    #print(num)
    pred.write(str(int(num>0))+' : ' + str(pred_values[i]) + '\n')
    res.append(int(num>0))

count = 0
for i in range(len(res)):
    #print("{a} : {b}".format(a=res[i], b=pred_values[i]))
    if (res[i] == pred_values[i]):
        count += 1
print(count)
pred.write("\n\n RES:  " + str(count))
pred.close()

