import random
import sys
import json

def randomizer(max, choose):
    new_max = max + 1;
    while (new_max > max):
        new_max = random.choice(choose);
    return new_max;

N = int(sys.argv[1]) if len(sys.argv) > 1 else 1
M = int(sys.argv[2]) if len(sys.argv) > 2 else 2
if len(sys.argv) > 3:
    Seed = int(sys.argv[3])
else:
    Seed = random.randrange(100000000)
    print(f"{Seed}", file=sys.stderr)
random.seed(Seed);

all_dots = ['a']

for i in range(N, M+1):
    
    test = open('./gen_ini/test{}.ini'.format(i), "w");
    test.close();
    
    motives = open("motives.txt", 'r')
    dot = 'a'
    while dot in all_dots:
        period = random.choice((60, 120, 240, 360, 720, 1440, 2880, 5760, 8640,10080));
        length = randomizer(period-1, (15, 30, 60, 120, 240, 360, 720, 1080, 1440))
        shift = randomizer(length-1, (0,30,60,120,240,360,540,720,1080))
        #shift = shift-1 if shift else 0
        attack = randomizer(shift if shift else 1, (0,15,30,45,60, 120))
        volume = random.choice((25,50,75,100, 125))
        dot = [period, length, shift, attack, volume]
    all_dots.append(dot)
    
    
    for line in motives:
        with open('./gen_ini/test{}.ini'.format(i), 'a') as f:
            f.write("[{}]\n".format(line[:-1]))
            #max_others = random.choice((60, 120, 1440, 10080));
            #max_others_two = randomizer(max_others, (30, 60, 120, 360, 720,  1440))
            #max_others_three = randomizer(max_others_two, (0,120,360,540,720,1080))
            #max_others_three = max_others_three-1 if max_others_three else 0
            f.write("period={}m\n".format(period))
            f.write("length={}m\n".format(length))
            f.write("shift={}m\n".format(shift))
            f.write("attack={}m\n".format(attack))
            f.write("volume={}G\n".format(volume))
