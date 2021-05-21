i = 0
final_res = open('new_res.txt', 'w')

with open('res_table.txt', 'r') as res:
    for line in res:
        if not(i%5):
            final_res.write(line)
        i += 1
