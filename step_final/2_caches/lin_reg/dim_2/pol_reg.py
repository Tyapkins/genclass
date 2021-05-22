import re
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.linear_model import Perceptron

patt = re.compile(r".*")
dots = []
Xs = []
testY, Ys = [], []
values = []

with open('./res_table.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        num = (b[-1]).replace(' ', '')
        a = b[0].split(', ')
        a = [int("".join([i for i in j if i.isdigit()])) for j in a]
        if not (((dot[0] <= 0.26) or (dot[0] >= 0.272))
        or ((dot[1] <= 0.26) or (dot[1] >= 0.272))):
            dots.append(np.array(a))
            values.append(int(num))
            testY.append(dot[2])

pred_values, pred_Ys, pred_dots = [], [], []
true_Y = []

with open('./true_table.txt', 'r') as res:
    for line in res:

        b = line.split(";")
        dot = b[2:5]
        for i in range(3):
            dot[i] = float(dot[i].replace(' ', ''))
        num = (b[-1]).replace(' ', '')
        a = b[0].split(', ')
        a = [int("".join([i for i in j if i.isdigit()])) for j in a]
        if not (((dot[0] <= 0.26) or (dot[0] >= 0.272))
        or ((dot[1] <= 0.26) or (dot[1] >= 0.272))):
            pred_dots.append(np.array(a))
            pred_values.append(int(num))
            true_Y.append(dot[2])

all_dots = dots + pred_dots

scorp = PCA(n_components=2)
scorp.fit(all_dots)
X_2D = scorp.transform(all_dots)

Xs = X_2D[:len(dots)]
Ys = testY

new_Xs = np.array(X_2D[len(dots):])
new_Ys = np.array(true_Y)

x = np.array(Xs)
y = np.array(Ys)

new_x = PolynomialFeatures(interaction_only=True).fit_transform(x).astype(int)
clf = Perceptron(fit_intercept=False, max_iter=10, tol=None,
                 shuffle=False).fit(new_x, values)

print(clf.score(new_x, values))
model = Pipeline([('poly', PolynomialFeatures(degree=2)),
                   ('linear', LinearRegression(fit_intercept=False))])

model = model.fit(x, y)
print(model.named_steps['linear'].coef_)

pred_Y = model.predict(new_Xs)


rmse = np.sqrt(mean_squared_error(new_Ys,pred_Y))
r2 = r2_score(new_Ys,pred_Y)

scr = model.score(new_Xs, true_Y)

for i in range(len(Xs)):
    if (Ys[i] >= 0):
        plt.plot(Xs[i][0], Xs[i][1], 'ro')
    else:
        plt.plot(Xs[i][0], Xs[i][1], 'bo')

for i in range(len(new_Xs)):
    if (new_Ys[i] >= 0):
        plt.plot(new_Xs[i][0], new_Xs[i][1], 'yo')
    else:
        plt.plot(new_Xs[i][0], new_Xs[i][1], 'go')

plt.show()

pred = open('./pol_prediction.txt', 'w')
pred.write('P : T\n\n\n')
res = []
for i, num in enumerate(pred_Y):
    pred.write(str(int(num>0))+' : ' + str(pred_values[i]) + '\n')
    res.append(int(num>0))

count = 0
for i in range(len(res)):
    if (res[i] == pred_values[i]):
        count += 1
print(count)
pred.write("\n\n RES:  " + str(count))
pred.close()

