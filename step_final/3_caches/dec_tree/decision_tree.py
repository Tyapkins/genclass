import json
import re
import sys
import operator

from random import choice
from random import seed
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

from sklearn.tree import DecisionTreeClassifier

RSEED = 100

tree = DecisionTreeClassifier(random_state=RSEED)

MAX_VAL = 2
#seed(100)

def metrics(a, b):
    res = 0
    for i, num in enumerate(a):
        res += ((num-b[i])/(max_mas[i]))**2
    return res
    
   
#def prediction(values):
#    mas = [0 for i in range(MAX_VAL+1)]
#    for val in values:
#        mas[val] += 1
#    new_mas = []
#    for i in range(MAX_VAL+1):
#        if mas[i] == max(mas):
#            new_mas.append(i)
#    return choice(new_mas)

patt = re.compile(r"\'.*\'")
time_patt_ini = re.compile(r"(period|length|shift|attack)=(?P<num>[\d]+m)")
size_patt_ini = re.compile(r"volume=(?P<num>[\d]+G)")
max_mas = [10080, 1440, 1080, 120, 125]

CHECK_DOTS_FROM = int(sys.argv[1]) if len(sys.argv) > 1 else 1001
CHECK_DOTS_TO = int(sys.argv[2]) if len(sys.argv) > 2 else 1100
K = int(sys.argv[3]) if len(sys.argv) > 3 else 1
known_dots = []
dots = []
values = []

for i in range(CHECK_DOTS_FROM, CHECK_DOTS_TO+1):
    all_attrs = []
    with open ('../../../step_ini/gen_ini/test' + str(i) + '.ini', 'r') as dot_file:
        for line in dot_file:
            if time_patt_ini.search(line):
                new_num = time_patt_ini.search(line).group("num")
                all_attrs.append(int(new_num[:-1]))
            elif size_patt_ini.search(line):
                new_num = size_patt_ini.search(line).group("num")
                all_attrs.append(int(new_num[:-1]))
                break
    dots.append(all_attrs)


with open('res_table.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        num = (b[-1]).replace(' ', '')
        values.append(int(num))
        a = patt.search(line)
        mas = a[0].split(", ")
        new_mas = [int(a[1:-2]) for a in mas]
        known_dots.append(new_mas)

X = np.array(known_dots)
y = np.array(values)

pred_val = []

tree.fit(X, y)

print('Check Accuracy:', tree.score(X, y))
print(tree.get_depth())

with open('true_table.txt', 'r') as f:
    for line in f:
        b = line.split(";")
        num = (b[-1]).replace(' ', '')
        pred_val.append(int(num))
        #a = patt.search(line)
        #mas = a[0].split(", ")
        #new_mas = [int(a[1:-2]) for a in mas]
        #known_dots.append(new_mas)

print('Model Accuracy:', tree.score(dots, pred_val))

#new_y = tree.predict(dots)
#print(new_y)
