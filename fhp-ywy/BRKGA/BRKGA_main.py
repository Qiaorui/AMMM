# imports
from __future__ import print_function
import math
import matplotlib.pyplot as plt
import time
import argparse
from DATParser import DATParser
from ValidateConfig import ValidateConfig


import BRKGA as brkga # BRKGA framework (problem independent)
import DECODER_per_hour as decoder # Decoder algorithm (problem-dependent)
#from DATA_1 import data # Input data (problem-dependent and instance-dependent)
from CONFIGURATION import config # Configuration parameters (problem-dependent and execution-dependent)


def showResult(sol):
    #print(sol)
    schedulePerHour = dict()
    for h in xrange(data.hours):
        schedulePerHour[h] = [0] * data.numNurses
    for h in xrange(data.hours):
        for n in xrange(data.numNurses):
            schedulePerHour[h][n] = sol[n][h]
    if None != sol:
        for n in xrange(data.numNurses):
            print("Nurse ", end='')
            if (n < 9):
                print(" ", end='')
            print(str(n+1) + " works:  ", end='')
            minHour = -1
            maxHour = -1
            totalHours = 0
            for h in xrange(data.hours):
                if sol[n][h] == 1:
                    totalHours += 1
                    print("  W", end='')
                    if (minHour == -1):
                        minHour = h
                    maxHour = h
                else:
                    print("  .", end='')
            if (minHour != -1):
                print("  Presence: " + str(maxHour - minHour + 1), end='')
            else:
                print("  Presence: 0", end='')
            print ("\t(TOTAL " + str(totalHours) + "h)")
        print("\n")
        print("Demand:          ", end='')

        for h in xrange(data.hours):
            if data.demand[h] < 10:
                print(" ", end='')
            print(" " + str(data.demand[h]), end='')
        print("\n")
        print("Assigned:        ", end='')
        for h in xrange(data.hours):
            total = sum(schedulePerHour[h])
            if (total < 10):
                print(" ", end='')
            print(" " + str(total), end='')
        workingNurse = 0
        for n in xrange(data.numNurses):
            if sum(sol[n]) > 0:
                workingNurse += 1
        print('\n#Nurse that works: ' + str(workingNurse))
    else:
        print("No result found")

# initializations
numIndividuals=int(config['numIndividuals'])
print(numIndividuals)
numElite=int(math.ceil(numIndividuals*config['eliteProp']))
numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
numCrossover=max(numIndividuals-numElite-numMutants,0)
maxNumGen=int(config['maxNumGen'])
ro=float(config['inheritanceProb'])
evol=[]

argp = argparse.ArgumentParser(description='GRASP')
argp.add_argument('dataFile', help='data file path')
args = argp.parse_args()

print('AMMM Project - BRKGA')
print('-----------------------')

# Parse data file
print('Reading Data file %s...' % args.dataFile)
data = DATParser.parse(args.dataFile)
ValidateConfig.validate(data)
print(data.__dict__)

# Main body
chrLength=decoder.getChromosomeLength(data)
print(chrLength)

population=brkga.initializePopulation(numIndividuals,chrLength)

i=0

while (i<maxNumGen):
    print(i)
    start = time.time()
    population = decoder.decode(population,data)
    evol.append(brkga.getBestFitness(population)['fitness'])
    if numElite>0:
        elite, nonelite = brkga.classifyIndividuals(population,numElite)
    else: 
        elite = []
        nonelite = population
    if numMutants>0: mutants = brkga.generateMutantIndividuals(numMutants,chrLength)
    else: mutants = []
    if numCrossover>0: crossover = brkga.doCrossover(elite,nonelite,ro,numCrossover)
    else: crossover=[]
    population=elite + crossover + mutants
    i+=1
    print(time.time() - start)

population = decoder.decode(population, data)
bestIndividual = brkga.getBestFitness(population)
plt.plot(evol)
plt.xlabel('number of generations')
plt.ylabel('Fitness of best individual')
plt.axis([0, len(evol), 0, data.numNurses])
plt.show()

showResult(bestIndividual['solution'])
print(bestIndividual['fitness'])