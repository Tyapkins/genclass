import json
from collections import Counter

with open('table.json', 'r') as table:
    data = json.load(table)

stats = Counter()

for req in data.values():
    for attr in req:
        if (attr != "size"):
            stats[str(attr)+":"+str(req[attr])]  += 1
with open('res.txt', 'w') as f:
    for motive, num in stats.most_common():
        f.write(motive + ' - ' + str(num) + '\n')
