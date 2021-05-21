import sys

K = int(sys.argv[1]) if len(sys.argv) > 1 else 3

final_res = open('pred_res.txt', 'w')

for K in range(1, 51):
    dots = []
    values = []
    with open('./preds/prediction' + str(K) + '.txt', 'r') as res:
        for line in res:
            b = line.split(":")
            for a in b:
                b[b.index(a)] = ''.join(c for c in a if ((c != ' ') and (c != '\n')))
            mas = (b[0][1:-1]).split(',')
            mas = [int(a) for a in mas]
            dots.append(mas)
            values.append(int(b[1]))

    true_dots = []
    true_vals = []
    with open('true_table.txt', 'r') as check:
        for line in check:
            b = line.split(";")
            num = (b[-1]).replace(' ', '')
            true_vals.append(int(num))
            newsim = ''.join(c for c in b[0] if (c.isdigit() or (c==',')))
            newsim = newsim.split(",")
            newsim = [int(a) for a in newsim]
            true_dots.append(newsim)
    sum = 0
    for i, dot in enumerate(dots):
        if values[i] == true_vals[true_dots.index(dot)]:
            sum += 1

    final_res.write("{a:4} : {b:4}\n".format(a=K, b=sum))
