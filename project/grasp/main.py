#!/usr/bin/python
from GRASP import Grasp
import re


def parse_data(data):
    config = {}
    for s in data.split(';'):
        ss = [x.strip() for x in s.split('=')]
        if len(ss) == 1:
            continue
        config[ss[0]] = int(ss[1]) if ss[1].isdigit() else [int(i) for i in re.findall(r'\d+', ss[1])]
    return config


def main():
    with open("../benchmark/x_20_0.dat", "r") as f:
        data = f.readlines()
        data = "".join([x.strip() for x in data])
    d = parse_data(data)
    g = Grasp(d)
    print(g)
    sol = g.solve(remaining_iterations=100, alpha=0.2, seed=7)
    print("finish")
    for s in sol["schedule"]:
        print(s)
    print("cost ", sol["cost"])


if __name__ == "__main__":
    main()