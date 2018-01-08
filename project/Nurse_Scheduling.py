import math


class NurseScheduling:

    def __init__(self, data=None):
        self.numNurses, self.hours, self.demand, self.minHours, self.maxHours, self.maxConsec, self.maxPresence, \
            self.combSize, self.verbose, self.raw_data = (None,)*10
        if data:
            self.read_input(data)

    def __str__(self):
        return ("numNurses = {0};\n"
                "hours = {1};\n" 
                "demand = {2};\n"
                "minHours = {3};\n"
                "maxHours = {4};\n"
                "maxConsec = {5};\n"
                "maxPresence = {6};").format(self.numNurses, self.hours, self.demand.__str__().replace(",", ""),
                                             self.minHours, self.maxHours, self.maxConsec, self.maxPresence)

    def __repr__(self):
        return self.__str__()

    def read_input(self, data):
        self.raw_data = data
        self.numNurses = data["numNurses"]
        self.hours = data["hours"]
        self.demand = data["demand"]
        self.minHours = data["minHours"]
        self.maxHours = data["maxHours"]
        self.maxConsec = data["maxConsec"]
        self.maxPresence = data["maxPresence"]

    @staticmethod
    def cost(schedule):
        if not schedule:
            return math.inf
        used = 0
        for nurse in schedule:
            for h in nurse:
                if h:
                    used += 1
                    break
        return used

    def generate_solution(self, schedule, demand):
        return {"schedule": schedule, "cost": self.cost(schedule), "demand": demand}

    def clear_solution(self, schedule, demand):
        surplus = []
        for i, nurse in enumerate(schedule):
            found = all([k < 0 for j, k in zip(nurse, demand) if j])
            if found:
                for j, works in enumerate(nurse):
                    if works:
                        demand[j] += 1
                surplus.append(i)
        surplus.sort(reverse=True)
        for index in surplus:
            del schedule[index]
        return self.generate_solution(schedule, demand)

    def generate_combinations(self, comb, remaining_size, remaining_consec, remaining_time, rest):
        candidates = []
        if not remaining_size:
            if self.maxHours - remaining_time >= self.minHours:
                comb2 = comb[:]
                candidates.append(comb)
                if comb2[-1] == 0:
                    comb2.insert(0, comb2.pop())
                    candidates.append(comb2)
        elif not remaining_time:
            comb.extend([0] * remaining_size)
            candidates.append(comb[:])
            while comb[-1] == 0:
                comb.insert(0, comb.pop())
                candidates.append(comb[:])
        elif not remaining_consec:
            comb.append(0)
            candidates.extend(
                self.generate_combinations(comb, remaining_size - 1, self.maxConsec, remaining_time, True))
        elif rest:
            comb.append(1)
            candidates.extend(
                self.generate_combinations(comb, remaining_size - 1, remaining_consec - 1, remaining_time - 1, False))
        else:
            comb2 = comb[:]
            comb.append(0)
            candidates.extend(
                self.generate_combinations(comb, remaining_size - 1, self.maxConsec, remaining_time, True))

            comb2.append(1)
            candidates.extend(
                self.generate_combinations(comb2, remaining_size - 1, remaining_consec - 1, remaining_time - 1, False))

        return candidates
