import numpy as np
import math, sys

def getChromosomeLength(data):
    return int(len(data["T"]))

def decode(population, data):
    print(population)
    for ind in population:
        solution, fitness=decoder_assignment(data,ind['chr'])
        ind['solution']=solution
        ind['fitness']=fitness    
    return(population)
    
def decoder_assignment(data,chromosome):
    C=map(float,data["C"][:])
    Caux=C[:]
    #print(Caux)
    T=map(float,data["T"][:])
    cost=map(float,data["cost"][:])
    solution=[None]*len(T)
    rem=1
    segment=1/float(len(C))
    used=[0]*len(C)
    
    for i in range(len(T)):
        j=int(math.floor(chromosome[i]/segment)) 
        if(C[j]-T[i]<0): return None, sys.maxint
        if used[j]==0: used[j]=1
        solution[i]=j
        C[j]-=T[i]
        if rem>(C[j]/Caux[j]): rem=(C[j]/Caux[j])
    
    fitness=sum(np.multiply(used,cost))+rem
    return solution, fitness
