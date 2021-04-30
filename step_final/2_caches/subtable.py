import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1001
M = int(sys.argv[2]) if len(sys.argv) > 2 else 1100
final_res = open('res' + str(N) + '-' + str(M) + '.txt', 'w')

i = 1

with open('final_table_0.15_1-4495.txt', 'r') as res:
    for line in res:
        if (N <= i <= M):
            final_res.write(line)
        i += 1
