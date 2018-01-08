#!/usr/bin/python
from grasp.GRASP import Grasp
import re
import os
import glob
import argparse


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


def run_grasp(data):
    grasp = Grasp(data)
    solution = grasp.solve(remaining_iterations=10, alpha=0.2, seed=7, timeout=10)
    return solution

def run_brkga(data):
    return {}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs='+', help="input file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument("-w", "--write", action="store_true", help="write to file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--grasp", action="store_true", help="use GRASP algorithm")
    group.add_argument("-b", "--brkga", action="store_true", help="use BRKGA algorithm")
    args = parser.parse_args()

    input_path = []
    for pattern in args.path:
        input_path.extend(glob.glob(pattern))
    input_path.sort(key=sort_function)

    if args.write:
        output = open("grasp_result.txt", "a")

    for path in input_path:
        with open(path, "r") as f:
            data = f.readlines()
            data = "".join([x.strip() for x in data])
            print(f.name, end=', ')
        d = parse_data(data)
        sol = run_grasp(d) if args.grasp else run_brkga(d)
        print(sol["cost"], ",", sol['time'])
        if args.verbose:
            for nurse in sol['schedule']:
                print(nurse)
        if args.write:
            output.write(os.path.basename(path) + ", " + str(sol['cost']) + ", " + str(sol['time']) + "\n")

    if args.write:
        output.close()


if __name__ == "__main__":
    main()
