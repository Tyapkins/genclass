import random
import sys
import json

def randomizer(max, choose):
    new_max = max + 1;
    while (new_max > max):
        new_max = random.choice(choose);
    return new_max;

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
K = int(sys.argv[2]) if len(sys.argv) > 2 else 1;
L = int(sys.argv[3]) if len(sys.argv) > 3 else 4;
if len(sys.argv) > 4:
    Seed = int(sys.argv[4])
else:
    Seed = random.randrange(100000000)
    print(f"{Seed}", file=sys.stderr)
random.seed(Seed);

with open('../table.json', 'r') as fh:
    data = json.load(fh);

reqs  = list(data.keys());
max_len = len(reqs)-1;
all_motives_list = [""]

for i in range(N+1):
    test = open('./gen_ini/test{}.ini'.format(i), "w");
    test.close();
    
    for j in range (L):
        res = ""
        motive_list = [""]
        subres = ""

        while res in all_motives_list:
            for k in range(K):
                while subres in motive_list:
                    chosen_req = reqs[random.randint(0, max_len)]
                    chosen_dict = data[chosen_req];
                    chosen_attr = list(chosen_dict.keys())[random.randint(0,      len(chosen_dict)-2)]
                    subres = "'{a}'='{b}'".format(a = chosen_attr, b =   chosen_dict[chosen_attr])
                    res += "{},".format(subres)
                motive_list.append(subres)
        all_motives_list.append(res)
        with open('./gen_ini/test{}.ini'.format(i), 'a') as f:
            f.write("[{}]\n".format(res[:-1]))
            max_others = random.choice((60, 120, 1440, 10080));
            max_others_two = randomizer(max_others, (30, 60, 120, 360, 720,  1440))
            max_others_three = randomizer(max_others_two, (0,120,360,540,720,1080))
            max_others_three = max_others_three-1 if max_others_three else 0
            f.write("period={}m\n".format(max_others));
            f.write("length={}m\n".format(max_others_two));
            f.write("shift={}m\n".format(max_others_three));
            f.write("attack={}m\n".format(randomizer(max_others_three, (0,15,120))));
            f.write("volume={}G\n".format(random.choice((50,100))));
