import numpy as np
import math, sys

def getChromosomeLength(data):
    return int(data.hours)

def decode(population, data):
    for ind in population:
        solution, fitness=decoder_per_hour(data,ind['chr'])
        ind['solution']=solution
        ind['fitness']=fitness
    return(population)

def simpleCheck(hoursAssignment, config):
    # Check maxPresence, maxHours, maxConsec
    # print(hoursAssignment)
    if sum(hoursAssignment) > 0:
        firstWorkingHour = hoursAssignment.index(1)
        lastWorkingHour = len(hoursAssignment) - 1 - hoursAssignment[::-1].index(1)
        """ 1. Check whether he/she exceeds the maxPresence """
        if lastWorkingHour - firstWorkingHour + 1 > config.maxPresence:
            return False
        workingHours = sum(hoursAssignment)
        """ 2. Check whether he/she exceeds the maxHours """
        if workingHours > config.maxHours:
            return False
        consecutiveHours = 0
        maxConsecNeedAdaption = False
        # range [firstWorkingHour, lastWorkingHour]
        for h in xrange(firstWorkingHour, lastWorkingHour + 1):
            # if nurse works at hour h
            if hoursAssignment[h] == 1:
                consecutiveHours += 1
                """ 3. Check whether he/she exceeds the maxConsec """
                if consecutiveHours > config.maxConsec:
                    return False
            # if nurse rests at hour h
            else:
                consecutiveHours = 0
    return True

def checkMinHours(hoursAssignment, config):
    if sum(hoursAssignment) > 0:
        workingHours = sum(hoursAssignment)
        """ Check whether he/she does not reach the minHours """
        if workingHours < config.minHours:

            return False
    return True

def checkConsecutiveRest(hoursAssignment, config):
    if sum(hoursAssignment) > 0:
        firstWorkingHour = hoursAssignment.index(1)
        lastWorkingHour = len(hoursAssignment) - 1 - hoursAssignment[::-1].index(1)
        workingHours = sum(hoursAssignment)
        maxConsecNeedsAdaption = False
        # range [firstWorkingHour, lastWorkingHour]
        for h in xrange(firstWorkingHour, lastWorkingHour + 1):
            # if nurse rests at hour h
            if hoursAssignment[h] == 0:
                """ Check whether he/she rests consecutively """
                if hoursAssignment[h + 1] == 0:
                    maxConsecNeedsAdaption = True
        if maxConsecNeedsAdaption:
            auxHoursAssignment = list(hoursAssignment)
            # Try to add hours [1 0 0 0 1] -> [1 0 1 0 1]
            # First check floor(lastWorkingHour - firstWorkingHour)/2 + workingHours <= maxHours since we want
            if math.floor((lastWorkingHour - firstWorkingHour)/2.0) + workingHours > config.maxHours:
                return False, None
            # Store index of hour to add
            correctionHours = list()
            for i in range(2, lastWorkingHour - firstWorkingHour, 2):
                auxHoursAssignment[firstWorkingHour + i] = 1
                if simpleCheck(auxHoursAssignment, config):
                    correctionHours.append(firstWorkingHour + i)
                else:
                    return False, None
            return True, correctionHours
        else:
            return True, None
    return True, None

def decoder_per_hour(data,chromosome):
    demand = list(data.demand)
    numNurses = data.numNurses
    # [[0,1...],...], list of list for each nurse
    solution = [[0 for i in xrange(len(demand))] for j in xrange(numNurses)]
    used = [0] * numNurses
    hour_ordered = sorted(range(data.hours), key=lambda k: chromosome[k])
    print(hour_ordered)
    for hour in hour_ordered:
        # Discard hours that have no demand
        print('hour: '+ str(hour))
        if demand[hour] <= 0:
            continue
        # Order the nurse, preferable if she's already working, ascending by the id
        workingNurses = list()
        notWorkingNurses = list()
        for idx, isUsed in enumerate(used):
            if isUsed:
                workingNurses.append(idx)
            else:
                notWorkingNurses.append(idx)
        nurses = workingNurses + notWorkingNurses
        for nurseId in nurses:
            # Discard if nurse has already been assigned to this hour in previous steps
            if solution[nurseId] == 1:
                continue
            aux = list(solution[nurseId])
            aux[hour] = 1
            # If this nurse is does not violate working at this hour
            if simpleCheck(aux, data):
                res, correctionHours = checkConsecutiveRest(aux, data)
                if res:
                    demand[hour] -= 1
                    print(demand[hour])
                    solution[nurseId][hour] = 1
                    print('nurse: '+str(nurseId))
                    print(solution[nurseId])
                    used[nurseId] = 1

                    if None != correctionHours:
                        print('nurseId: '+ str(nurseId))
                        count = 0
                        print(correctionHours)
                        for hh in correctionHours:
                            print('hour to do --demand' + str(hh))
                            count += 1
                            print(count)
                            solution[nurseId][hh] = 1
                            demand[hh] -= 1
                            print(demand[hh])
            #else:
                #print('aux failes')
                #print(aux)
            if demand[hour] <= 0:
                break
    print('demand')
    print(demand)

    for d in demand:
        if d > 0:
            return None, sys.maxint
    print('real demand')
    print(data.demand)
    schedulePerHour = [[0]*data.numNurses for i in xrange(data.hours)]

    for nurseId in xrange(numNurses):
        if not simpleCheck(solution[nurseId], data):
            return None, sys.maxint
        res, correctionHours = checkConsecutiveRest(solution[nurseId], data)
        if None != correctionHours:
            print('final change?')
        if not res:
            return None, sys.maxint
    print('assigned demand')
    for h in xrange(data.hours):
        schedulePerHour[h] = [0] * data.numNurses
    for h in xrange(data.hours):
        for n in xrange(data.numNurses):
            schedulePerHour[h][n] = solution[n][h]
    auxL = [sum(ll) for ll in schedulePerHour]
    print(auxL)
    print('remaining demand')
    print([i - j for i, j in zip(data.demand, [sum(ll) for ll in schedulePerHour])])
    fitness = sum(used)
    #print(solution)
    return solution, fitness
