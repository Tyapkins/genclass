import sys

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
M = int(sys.argv[2]) if len(sys.argv) > 2 else 2
table_name = ("./tables/table_"+sys.argv[3]+"_") if len(sys.argv) > 3 else "final_table"
final_name = ("final_table_"+sys.argv[3]+"_"+sys.argv[1]+"-"+sys.argv[2]+".txt") if len(sys.argv) > 3 else "final_table.txt"
to_write = open(final_name, "w")
for i in range(N, M+1):
    table_read = open(table_name+str(i)+".txt", "r")
    table_last = table_read.readlines()[-1]
    to_write.write(table_last)
table_read.close()
to_write.close()
