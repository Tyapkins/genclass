import sys
import re

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2;

patt = re.compile("[\d\.]+");
patt_ini = re.compile(r"\'(?P<attr>[a-z0-9]+)\'=(?P<vals>\[?(\'[a-z0-9]+\',? ?)+\]?)")

final = open("final_table.txt", "w");
final.close();
final = open("final_table.txt", "a");

for i in range(N):
    
    all_attrs = []
    
    lru_read = open("../step_caches/lru_out/lru_out"+str(i)+".txt", "r")
    lru_last = lru_read.readlines()[-1]
    lru_read.close()

    scache_read = open("../step_caches/scache_out/scache_out"+str(i)+".txt", "r");
    scache_last = scache_read.readlines()[-1];
    scache_read.close();

    attrs_read = open("../step_ini/gen_ini/test"+str(i)+".ini", "r")
    for line in attrs_read:
        if patt_ini.search(line):
            all_attrs.append(line[1:-2].replace("'", ''))

          
    lru_BHR = float(patt.search(lru_last).group());
    scache_BHR = float(patt.search(scache_last).group());
    
    final.write("{A} | {L} | {S} | {C}\n".format(A = all_attrs, L = lru_BHR, S = scache_BHR, C = int(scache_BHR > lru_BHR)))
print("THAT'S ALL FOLKS!");
final.close();
