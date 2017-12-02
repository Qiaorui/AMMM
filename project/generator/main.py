#!/usr/bin/python
import random
import sys
from nurseTest import Instance

"""
// A
numNurses = 20;
hours = 24;
demand = [2 2 1 1 1 2 2 3 4 6 6 7 5 8 8 7 6 6 4 3 4 3 3 3];
minHours = 5;
maxHours = 9;
maxConsec = 3;

// B
maxPresence = 14;



hours >= maxHours >= minHours
hours >= maxConsec >= maxHours
hours >= maxPresence >= maxConsec
minHours means nothing
mininium Nurse = demand.max * (hours / maxHours )

maxPresence <= maxHours*2-2

"""


"""
Input:
% occupancy
number of minimum nurse
numNurse
"""





def main():
    random.seed(7)
    i = Instance()
    print(i.numNurses)




if __name__ == "__main__":
    main()
