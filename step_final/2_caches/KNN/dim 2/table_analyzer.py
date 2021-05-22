import re
import sys
from random import choice
from random import seed

from sklearn.decomposition import PCA

seed(100)

def metrics(a, b):
    res = 0
    for i, num in enumerate(a):
        res += ((num-b[i])/(max_mas[i]))**2
    return res

patt = re.compile(r"\'.*\'")
time_patt_ini = re.compile(r"(period|length|shift|attack)=(?P<num>[\d]+m)")
size_patt_ini = re.compile(r"volume=(?P<num>[\d]+G)")
max_mas = [10080, 1440, 1080, 120, 125]

CHECK_DOTS_FROM = int(sys.argv[1]) if len(sys.argv) > 1 else 1001
CHECK_DOTS_TO = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
K = int(sys.argv[3]) if len(sys.argv) > 3 else 1
known_dots = []
dots = []
values = []

for i in range(CHECK_DOTS_FROM, CHECK_DOTS_TO+1):
    all_attrs = []
    with open ('../../../../step_ini/gen_ini/test' + str(i) + '.ini', 'r') as dot_file:
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

all_dots = known_dots + dots;

scorp = PCA(n_components=2)
scorp.fit(all_dots)
X_2D = scorp.transform(all_dots)

X = list(X_2D[:len(known_dots)])
new_X = list(X_2D[len(known_dots):])
y = values
for i in range(len(X)):
    X[i] = list(X[i])
for i in range(len(new_X)):
    new_X[i] = list(new_X[i])



for K in range(1, 51):
    pred = open('./preds/prediction' + str(K) + '.txt', 'w')
    for i, dot in enumerate(new_X):
        super_num_metrics = {X.index(a): metrics(dot,a) for a in X}

        sorted_metrics = sorted(super_num_metrics, key = lambda i: super_num_metrics[i])

        pred_mas = [values[sorted_metrics[k]] for k in range(K)]
        sum = 0
        for k in range(K):
            sum += values[sorted_metrics[k]]
        val = 0 if (sum < K//2) else (1 if (sum > K//2) else choice([0,1]))
        pred.write("{a:30} : {b:4}\n".format(a = str(dots[i]), b = val))
    pred.close()

exit(0)

for K in range(1, 51):
    pred = open('./preds/prediction' + str(K) + '.txt', 'w')
    for dot in dots:
        super_num_metrics = {known_dots.index(a): metrics(dot,a) for a in known_dots}

        sorted_metrics = sorted(super_num_metrics, key = lambda i: super_num_metrics[i])

        pred_mas = [values[sorted_metrics[k]] for k in range(K)]
        sum = 0
        for k in range(K):
            sum += values[sorted_metrics[k]]
        val = 0 if (sum < K//2) else (1 if (sum > K//2) else choice([0,1]))
        pred.write("{a:30} : {b:4}\n".format(a = str(dot), b = val))
    pred.close()

