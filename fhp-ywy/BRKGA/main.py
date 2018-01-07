# imports
import math
import matplotlib.pyplot as plt
import time

import BRKGA as brkga # BRKGA framework (problem independent)
import DECODER_assignment as decoder # Decoder algorithm (problem-dependent)
from DATA_1 import data # Input data (problem-dependent and instance-dependent)
from CONFIGURATION import config # Configuration parameters (problem-dependent and execution-dependent)

# initializations
numIndividuals=int(config['numIndividuals'])
print(numIndividuals)
numElite=int(math.ceil(numIndividuals*config['eliteProp']))
numMutants=int(math.ceil(numIndividuals*config['mutantProp']))
numCrossover=max(numIndividuals-numElite-numMutants,0)
maxNumGen=int(config['maxNumGen'])
ro=float(config['inheritanceProb'])
evol=[]

# Main body
chrLength=decoder.getChromosomeLength(data)
print(chrLength)

population=brkga.initializePopulation(numIndividuals,chrLength)

i=0

while (i<maxNumGen):
    print i
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
plt.axis([0, len(evol), 0, sum(data["cost"])+5])
plt.show()

print bestIndividual
