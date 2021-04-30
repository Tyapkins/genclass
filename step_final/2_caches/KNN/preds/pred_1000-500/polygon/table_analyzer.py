import json
import re
import sys
from random import choice
from collections import Counter


patt = re.compile(r"\'.*\'")
#dot_patt = re.compile("(\d+) \: ((0|1)\.\d+)")
time_patt_ini = re.compile(r"(period|length|shift|attack)=(?P<num>[\d]+m)")
size_patt_ini = re.compile(r"volume=(?P<num>[\d]+G)")
max_mas = [10080, 1440, 1080, 120, 125]

def metrics(a, b):
    res = 0
    for i, num in enumerate(a):
        res += ((num-b[i])/(max_mas[i]))**2
    return res

CHECK_DOTS_FROM = int(sys.argv[1]) if len(sys.argv) > 1 else 1001
CHECK_DOTS_TO = int(sys.argv[2]) if len(sys.argv) > 2 else 1100
K = int(sys.argv[3]) if len(sys.argv) > 3 else 1
known_dots = []
dots = []
values = []

for i in range(CHECK_DOTS_FROM, CHECK_DOTS_TO+1):
    all_attrs = []
    with open ('../ResGen/step_ini/gen_ini/test' + str(i) + '.ini', 'r') as dot_file:
        for line in dot_file:
            if time_patt_ini.search(line):
                new_num = time_patt_ini.search(line).group("num")
                all_attrs.append(int(new_num[:-1]))
            elif size_patt_ini.search(line):
                new_num = size_patt_ini.search(line).group("num")
                all_attrs.append(int(new_num[:-1]))
                break
    #print(all_attrs)
    dots.append(all_attrs)


#with open ('final_table_0.15.txt', 'r') as file_dot:
#    for line in file_dot:
#        a = patt.search(line)
#        mas = a[0].split(", ")
#        new_mas = [int(a[1:-2]) for a in mas]
#        dots.append(new_mas)
with open('res_table.txt', 'r') as res:
    for line in res:
        b = line.split(";")
        num = (b[5])[1:-2]
        values.append(int(num))
        a = patt.search(line)
        mas = a[0].split(", ")
        new_mas = [int(a[1:-2]) for a in mas]
        known_dots.append(new_mas)
#print(known_dots)
#nulls = [a for a in known_dots if values[known_dots.index(a)] == 0]

for K in range(1, 501):
    pred = open('prediction' + str(K) + '.txt', 'w')
    for dot in dots:
        # num_metrics = [metrics(dot, a) for a in known_dots]
        super_num_metrics = {known_dots.index(a): metrics(dot,a) for a in known_dots}
        sorted_metrics = sorted(super_num_metrics, key = lambda i: super_num_metrics[i])
        sum = 0
        for k in range(K):
            sum += values[sorted_metrics[k]]
            val = 0 if (sum < K//2) else (1 if (sum > K//2) else choice([0,1]))
        pred.write("{a:30} : {b:4}\n".format(a = str(dot), b = val))
    pred.close()
