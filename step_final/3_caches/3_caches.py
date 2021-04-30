import sys
import re

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
M = int(sys.argv[2]) if len(sys.argv) > 2 else 2
table_name = ("./tables/table_"+sys.argv[3]+"_") if len(sys.argv) > 3 else "final_table"

patt = re.compile("(\d+) \: ((0|1)\.\d+)")
patt_ini = re.compile(r"\'(?P<attr>[a-z0-9]+)\'=(?P<vals>\[?(\'[a-z0-9]+\',? ?)+\]?)")
time_patt_ini = re.compile(r"(period|length|shift|attack)=(?P<num>[\d]+m)")
size_patt_ini = re.compile(r"volume=(?P<num>[\d]+G)")


for i in range(N, M+1):

    final = open(table_name + str(i) + ".txt", "w")
    final.close()
    final = open(table_name + str(i) + ".txt", "a")
    res = ""
    
    all_attrs = []
    
    lru_read = open("../step_caches/lru_out/lru_out"+str(i)+".txt", "r")

    lfu_read = open("../step_caches/lru2_out/lru2_out"+str(i)+".txt", "r")

    snlru_read = open("../step_caches/snlru_out/snlru_out"+str(i)+".txt", "r")

    attrs_read = open("../step_ini/gen_ini/test"+str(i)+".ini", "r")

    for line in attrs_read:
        if time_patt_ini.search(line):
            all_attrs.append(time_patt_ini.search(line).group("num"))
        elif size_patt_ini.search(line):
            all_attrs.append(size_patt_ini.search(line).group("num"))
            break

    last_lfu_BHR = 0
    last_snlru_BHR = 0

    line_num = sum(1 for line in lru_read)
    lru_read.close()
    lru_read = open("../step_caches/lru_out/lru_out"+str(i)+".txt", "r")
    for j in range(line_num):
        res = '{:^50}'.format('{}'.format(all_attrs))
        line = patt.search(lru_read.readline())
        lru_BHR, lfu_BHR, snlru_BHR, req_count = 0, 0, 0, 0
        if (line):
            req_count = int(line.group(1))
            lru_BHR = float(line.group(2))
            lfu_line = patt.search(lfu_read.readline())
            if (lfu_line):
                lfu_BHR = float(lfu_line.group(2))
                last_lfu_BHR = lfu_BHR
            else:
                lfu_BHR = last_lfu_BHR
            snlru_line = patt.search(snlru_read.readline())
            if (snlru_line):
                snlru_BHR = float(snlru_line.group(2))
                last_snlru_BHR = snlru_BHR
            else:
                snlru_BHR = last_snlru_BHR
        res_h = 2 if snlru_BHR > max(lru_BHR, lfu_BHR) else int(lru_BHR > lfu_BHR)
        res += " ; {C:^10} ; {R:^20} ; {F:^20} ; {S:^20} ; {h:2}\n".format(C=req_count, R=lru_BHR, F=lfu_BHR, S=snlru_BHR, h=res_h)
        final.write(res)
    final.close()
print("THAT'S ALL FOLKS!")
#final.close()
