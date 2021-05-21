import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree as Tree
from sklearn.decomposition import PCA

from sklearn.tree import DecisionTreeClassifier

RSEED = 100

tree = DecisionTreeClassifier(random_state=RSEED, max_depth=3)

MAX_VAL = 2
#seed(100)


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

all_dots = known_dots + dots


scorp = PCA(n_components=2)
scorp.fit(all_dots)
X_2D = scorp.transform(all_dots)

X = np.array(X_2D[:len(known_dots)])
y = np.array(values)

new_X = X_2D[len(known_dots):]
#print(len(new_X))
#print(len(X))
#exit(0)

pred_val = []

tree.fit(X, y)

print('Check Accuracy:', tree.score(X, y))
print(tree.get_depth())

with open('true_table.txt', 'r') as f:
    for line in f:
        b = line.split(";")
        num = (b[-1]).replace(' ', '')
        pred_val.append(int(num))

print('Model Accuracy:', tree.score(new_X, pred_val))
Tree.plot_tree(tree)
plt.show()