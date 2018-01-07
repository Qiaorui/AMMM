import numpy as np
import sys

def getChromosomeLength(data):
    return int(len(data["T"])+len(data["C"]))

def decode(population, data):
    for ind in population:
        solution, fitness=decoder_order(data,ind['chr'])
        ind['solution']=solution
        ind['fitness']=fitness    
    return(population)
    
def decoder_order(data,chromosome):
    C=map(float,data["C"][:])
    Caux=C[:]
    T=map(float,data["T"][:])
    cost=map(float,data["cost"][:])
    
    solution=[None]*len(T)
    rem=1
    used=[0]*len(C)
    
    chr_task=chromosome[0:len(T)]
    chr_computer=chromosome[len(T):len(chromosome)]
    
    task_order=sorted(range(len(T)), key=lambda k: chr_task[k])

    computer_order=sorted(range(len(C)), key=lambda k: chr_computer[k])

    for i in task_order:
        assigned=False
        for roundUsed in [True,False]:
            for j in computer_order:
                if(used[j]==roundUsed and C[j]-T[i]<0):continue
                if(used[j]==0): used[j]=1
                solution[i]=j
                C[j]-=T[i]
                if rem>(C[j]/Caux[j]): rem=(C[j]/Caux[j])
                assigned=True
                break
            if assigned: break
        if not assigned: return None, sys.maxint
    fitness=sum(np.multiply(used,cost))+rem
    return solution, fitness
