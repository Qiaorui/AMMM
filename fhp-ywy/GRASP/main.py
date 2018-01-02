from __future__ import print_function
import argparse, math, random
from DATParser import DATParser

maxIter = 1
alpha = 0
lambdaA = 100000 # Nurse not works, high penalization
lambdaB = 1000 #
lambdaC = 500
lambdaD = 100
lambdaE = 100


# Determine if the demand is satisfied with solution sol_h
def isDemandSatisfied(sol_h, demand):
    nursesUsed = set()
    print('-----Printing sol to check demand------')
    print(sol_h)
    for assignment in sol_h:
        nursesUsed.add(assignment['nurseId'])
    return len(nursesUsed) >= demand

# Check minHours, maxHours, maxConsec, maxPresence, demand, no consecutive rest
def isFeasible(sol):
    schedulePerNurse = dict()
    schedulePerHour = dict()
    # {nurse0: [0, 1, 0...], 1: [...] ...}
    for i in xrange(config.numNurses):
        schedulePerNurse[i] = [0] * config.hours
    # {hour0: [0, 1, 0...], 1: [...] ...}
    for i in xrange(config.hours):
        schedulePerHour[i] = [0] * config.numNurses

    for assignment in sol:
        schedulePerNurse[assignment['nurseId']][assignment['hour']] = 1
        schedulePerHour[assignment['hour']][assignment['nurseId']] = 1

    """ 1. Check whether all demands are satisfied """
    for hour, nursesAssignment in schedulePerHour.iteritems():
        if sum(nursesAssignment) < config.demand[hour]:
            return False
    """ Check other contraints for nurses that work """
    for nurseId, hoursAssignment in schedulePerNurse.iteritems():
        if sum(hoursAssignment) > 0:
            # First working hour
            firstWorkingHour = hoursAssignment.index(1)
            # Last working hour
            lastWorkingHour = len(hoursAssignment) - 1 - hoursAssignment[::-1].index(1)
            """ 2. Check whether he/she exceeds the maxPresence """
            if lastWorkingHour - firstWorkingHour + 1 > config.maxPresence:
                return False
            # A counter for minHours and maxHours
            workingHours = 0
            # A counter for maxConsec
            consecutiveHours = 0
            rested = False
            # range [firstWorkingHour, lastWorkingHour]
            for h in xrange(firstWorkingHour, lastWorkingHour + 1):
                # if nurse works at hour h
                if hoursAssignment[h] == 1:
                    workingHours += 1
                    consecutiveHours += 1
                    """ 3. Check whether he/she exceeds the maxConsec """
                    if consecutiveHours > config.maxConsec:
                        return False
                # if nurse rests at hour h
                else:
                    """ 4. Check whether he/she rests consecutively """
                    if hoursAssignment[h + 1] == 0:
                        return False
                    consecutiveHours = 0
            """ 5. Check whether he/she exceeds the minHours """
            if workingHours < config.minHours:
                return False
            """ 6. Check whether he/she exceeds the maxHours """
            if workingHours > config.maxHours:
                return False
    # No constraints are violated, which means the solution is feasible
    return True

# Compute the number of nurses that work
def computeCost(sol):
    usedNurse = set()
    for assignment in sol:
        usedNurse.add(assignment['nurseId'])
    return len(usedNurse)

def localSearch(sol):
    return sol

# Return a pair which consists of min and max greedy cost of the candidates
def getMinMax_gc(candidates):
    min_gc = max_gc = None
    for index, candidate in enumerate(candidates):
        print('-----Printing a candidate------')
        print(index)
        print(candidate)
        if index == 0:

            min_gc = candidate['gc']
            max_gc = candidate['gc']
        else:
            if candidate['gc'] < min_gc:
                min_gc = candidate['gc']
            if candidate['gc'] > max_gc:
                max_gc = candidate['gc']
    return min_gc, max_gc

# Compute the RCL
def getRCL(min_gc, max_gc, candidates):
    RCL = list()
    for candidate in candidates:
        if candidate['gc'] <= min_gc + (max_gc - min_gc) * alpha:
            RCL.append(candidate)
    return RCL

# Random select an element from the set
def randomSelection(elements):
    return elements[int(math.floor(random.random() * len(elements)))]

def getCandElementsAndGC(h, numNurses, sol):
    candidates = list()
    # We could possibly add a working hour to solve the problem caused by rest at previous hour
    # E = {< hour, nurse, gc >}
    # First iteration
    if h == 0:
        for nurse in xrange(numNurses):
            candidates.append({'hour': h, 'nurseId': nurse, 'gc': lambdaA})
    else:
        schedulePerNurse = dict()
        # {nurse0: [0, 1, 0...], 1: [...] ...}
        for i in xrange(config.numNurses):
            schedulePerNurse[i] = [0] * h
        for assignment in sol:
            schedulePerNurse[assignment['nurseId']][assignment['hour']] = 1
        for nurseId, hoursAssignment in schedulePerNurse.iteritems():
            # 2 cases, whether nurse works before
            workingHours = sum(hoursAssignment)
            " A nurse that is already working "
            if workingHours > 0:
                """ 1. Check whether he/she exceeds the maxHours """
                if workingHours + 1 > config.maxHours:
                    continue
                # First working hour
                firstWorkingHour = hoursAssignment.index(1)
                # Last working hour
                lastWorkingHour = len(hoursAssignment) - 1 - hoursAssignment[::-1].index(1)
                """ 2. Check whether he/she exceeds the maxPresence """
                # We check the length between first working and actual to see if it is possible to assign
                if h - firstWorkingHour + 1 > config.maxPresence:
                    continue
                # If len(hoursAssignment) < maxConsec at most, consecutive hours = maxConsec if we assign nurse to this hour, so we only check maxHours
                # Otherwise, we also have to check for maxConsec, we check last maxConsec positions of hoursAssignment to make sure that the sum is < maxConsec
                """ 3. Check whether he/she exceeds the maxConsec """
                if len(hoursAssignment) >= config.maxConsec:
                    if sum(hoursAssignment[-config.maxConsec:]) >= config.maxConsec:
                        continue
                """ 4. Check whether he/she will rest consecutively if he/she works at hour h """
                # If the distance between last working hour and actual hour is > 3, which means 1 0 0 0 h, then it is impossible
                restedButChanged = 0
                rested = 0
                distanceLastWHandH = h - lastWorkingHour
                if distanceLastWHandH > 3:
                    continue
                # 1 0 0 h, we could change last 0 (e.g. h - 1) to 1, we have also to modify the solution reflecting the change
                elif distanceLastWHandH == 3:
                    restedButChanged = 1
                    # modify the solution reflecting the change
                    sol.append({'hour': h - 1, 'nurseId': nurseId})
                elif distanceLastWHandH == 2:
                    rested = 1
                " If nurse works at this hour, all constraint will also be fulfilled, then we compute the greedy cost "
                greedyCost = -(lastWorkingHour - firstWorkingHour + 1) * lambdaB - (config.minHours - workingHours) * lambdaC - rested * lambdaD - restedButChanged * lambdaE
                candidates.append({'hour': h, 'nurseId': nurseId, 'gc': greedyCost})
            else:
                " A new nurse to work "
                candidates.append({'hour': h, 'nurseId': nurseId, 'gc': lambdaA})

    return candidates, sol

def greedeConsturctive(hours, numNurses, demand):
    sol = list()
    for h in xrange(hours):
        if config.demand[h] > 0:
            sol_h = list()
            candidates, newSol = getCandElementsAndGC(h, numNurses, sol)
            sol = newSol
            print('-----Printing all candidates------')
            print(candidates)
            while len(candidates) != 0:
                (min_gc, max_gc) = getMinMax_gc(candidates)
                print('-----Printing min and max------')
                print(min_gc)
                print(max_gc)
                RCL = getRCL(min_gc, max_gc, candidates)
                print('-----Printing RCL------')
                print(RCL)
                e = randomSelection(RCL)
                print('-----Printing selected element------')
                print(e)
                sol_h.append(e)
                if isDemandSatisfied(sol_h, demand[h]):
                    break
                "Update candidates"
                candidates = [x for x in candidates if x['nurseId'] != e['nurseId']]
                print('-----Printing updated candidates------')
                print (candidates)
            if not isDemandSatisfied(sol_h, demand[h]):
                return None, float("inf")
            sol = sol + sol_h
    if not isFeasible(sol):
        return None, float("inf")
    cost = computeCost(sol)
    return sol, cost

# Print result like CPLEX
def showResult(sol):
    schedulePerNurse = dict()
    schedulePerHour = dict()
    # {nurse0: [0, 1, 0...], 1: [...] ...}
    for i in xrange(config.numNurses):
        schedulePerNurse[i] = [0] * config.hours
    # {hour0: [0, 1, 0...], 1: [...] ...}
    for i in xrange(config.hours):
        schedulePerHour[i] = [0] * config.numNurses

    for assignment in sol:
        schedulePerNurse[assignment['nurseId']][assignment['hour']] = 1
        schedulePerHour[assignment['hour']][assignment['nurseId']] = 1
    for n in xrange(config.numNurses):
        print("Nurse ", end='')
        if (n < 10):
            print(" ", end='')
        print(str(n+1) + " works:  ", end='')
        minHour = -1
        maxHour = -1
        totalHours = 0
        for h in xrange(config.hours):
            if schedulePerNurse[n][h] == 1:
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

    for h in xrange(config.hours):
        if config.demand[h] < 10:
            print(" ", end='')
        print(" " + str(config.demand[h]), end='')
    print("\n")
    print("Assigned:        ", end='')
    for h in xrange(config.hours):
        total = sum(schedulePerHour[h])
        if (total < 10):
            print(" ", end='')
        print(" " + str(total), end='')

def run():
    # Parse arguments
    argp = argparse.ArgumentParser(description='GRASP')
    argp.add_argument('dataFile', help='data file path')
    args = argp.parse_args()

    print('AMMM Project - GRASP')
    print('-----------------------')

    # Parse data file
    print('Reading Data file %s...' % args.dataFile)
    global config
    config = DATParser.parse(args.dataFile)
    minCost = None
    minCostSol = None
    minCostSol, minCost = greedeConsturctive(config.hours, config.numNurses, config.demand)
    """
    for i in xrange(maxIter):
        # Constructive phase
        sol, cost = greedeConsturctive(config.hours, config.numNurses, config.demand)
        # Local search
        newSol, newCost = localSearch(sol)
        if None == minCost:
            minCost = newCost
            minCostSol = newSol
    """
    showResult(minCostSol)
if __name__ == '__main__':
    run()