i = 0
final_res = open('res_table.txt', 'w')

with open('new_table.txt', 'r') as res:
    for line in res:
        if not(i%5):
            final_res.write(line)
        i += 1
