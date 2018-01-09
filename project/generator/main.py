#!/usr/bin/python
import random
import os
from Generator import Instance

start = 8
end = 100
repetition = 10
seed = 7
directory = "./benchmark/"


def main():
    random.seed(seed)

    if not os.path.exists(directory):
        os.makedirs(directory)
    for i in range(start, end):
        for j in range(repetition):
            benchmark = Instance(i)
            with open(directory + "x_" + str(i) + "_" + str(j) + ".dat", 'w') as file:
                file.write(benchmark.__str__())
            print(benchmark)


if __name__ == "__main__":
    main()
