#!/usr/bin/python
from GRASP import Grasp
import re
import sys
import os
import glob


def parse_data(data):
    config = {}
    for s in data.split(';'):
        ss = [x.strip() for x in s.split('=')]
        if len(ss) == 1:
            continue
        config[ss[0]] = int(ss[1]) if ss[1].isdigit() else [int(i) for i in re.findall(r'\d+', ss[1])]
    return config


def sort_function(x):
    return int(''.join(re.findall(r'\d+', os.path.basename(x))))


def main():
    if len(sys.argv) < 2:
        print("usage:   python main.py f1 [f2 ...]")
        exit(1)

    input_path = []
    for arg in sys.argv[1:]:
        input_path.extend(glob.glob(arg))

    input_path.sort(key=sort_function)
    for i in input_path:
        print(i)

    output = open("grasp_result.txt", "a")
    for path in input_path:
        with open(path, "r") as f:
            data = f.readlines()
            data = "".join([x.strip() for x in data])
            print(f.name, end=', ')
        d = parse_data(data)
        g = Grasp(d)
        sol = g.solve(remaining_iterations=10, alpha=0.2, seed=7, timeout=10)
        print(sol["cost"], ",", sol['time'])
        output.write(os.path.basename(path) + ", " + str(sol['cost']) + ", " + str(sol['time']) + "\n")

    output.close()


if __name__ == "__main__":
    main()
