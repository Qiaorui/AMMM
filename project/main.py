#!/usr/bin/python
from grasp.GRASP import Grasp
from brkga.BRKGA import Brkga
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


def run_grasp(data, verbose=False):
    grasp = Grasp(data)
    if verbose:
        print(grasp)
    solution = grasp.solve(remaining_iterations=100, alpha=0.2, seed=7, timeout=600, verbose=verbose)
    return solution


def run_brkga(data, verbose=False):
    brkga = Brkga(data)
    if verbose:
        print(brkga)
    solution = brkga.solve(max_generations=100, num_individuals=100, elite_prop=0.15, mutant_prop=0.2,
                           inheritance_prop=0.7, timeout=600, verbose=verbose)
    return solution


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs='+', help="input file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
    parser.add_argument("-w", dest="output_file", action="store", help="write to file")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", "--grasp", action="store_true", help="use GRASP algorithm")
    group.add_argument("-b", "--brkga", action="store_true", help="use BRKGA algorithm")
    args = parser.parse_args()

    input_path = []
    for pattern in args.path:
        input_path.extend(glob.glob(pattern))
    input_path.sort(key=sort_function)

    for path in input_path:
        with open(path, "r") as f:
            data = f.readlines()
            data = "".join([x.strip() for x in data])
            print(f.name, end=', ')
        d = parse_data(data)
        sol = run_grasp(d, args.verbose) if args.grasp else run_brkga(d, args.verbose)
        if sol['found']:
            print(sol["cost"], ",", sol['time'])
        else:
            print("Not Found, best cost:", sol['cost'])
        if args.verbose:
            for nurse in sol['schedule']:
                print(nurse)
            print("demand:", sol['demand'])
        if args.output_file:
            with open(args.output_file, 'a') as output:
                output.write(os.path.basename(path) + ", " + str(sol['cost']) + ", " + str(sol['time']) + "\n")


if __name__ == "__main__":
    main()
