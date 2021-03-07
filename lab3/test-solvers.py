#!/usr/bin/env python3

import numpy as np
import glob, re, time

from sokobanUbuntu import *

solver = "seq-sat-fd-autotune-1"

solved = []
cost = []
start_time = time.time()

levels = range(1, 26)

solver_path = "./downward/fast-downward.py domain.pddl problem-out.pddl --overall-time-limit 60 --plan-file sas_plan --alias " + solver

for level in levels:
    filename = "./benchmarks/sasquatch/level%s.sok" %(level)

    # read file
    with open(filename, 'r') as file:
        board = SokobanGame(file.read().rstrip('\n'))

    # get instance
    resultingInstance = getProblemInstance(board)
    f = open('problem-out.pddl', "w")
    f.write(resultingInstance)
    f.close()

    # try to solve in < 60 seconds
    
    #os.system("./downward/fast-downward.py --overall-time-limit 60 --plan-file sas_plan --alias seq-sat-fdss-2 domain.pddl problem-out.pddl")
    os.system(solver_path)
    
    numbers = []
    all_files = glob.glob("./sas_plan*")
    for single_file in all_files:
        numbers.append(int(re.findall(r'\d+', single_file)[0]))

    if not numbers:
        solved.append(0)
        cost.append("inf")
    else:
        f_name = 'sas_plan.%s' %(np.max(numbers))
        with open(f_name, "r") as f:
            lines = f.read().split("\n")
        for line in lines:
            if "cost" in line:
                cost.append(line[2:-12])
        solved.append(1)
        f.close()

end_time = time.time() - start_time

string = "Solver: " + solver + "\n\n"
string += "Solved %s out of %s\n" %(np.sum(solved), len(solved))
string += "Process time: %s s\n\n" %(round(end_time,2))
for level in levels:
    string += "Level %s:" %(level)
    if (solved[level-1]):
        string += " SOLVED"
        string += " - " + cost[level-1] + "\n"
    else:
        string += " NOT SOLVED\n"

print("---------------------------")
print(string)

f = open('exec-result.txt', 'w')
f.write(string)
f.close()