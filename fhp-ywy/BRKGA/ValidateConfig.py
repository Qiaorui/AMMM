# Validate config attributes read from a DAT file.
class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['numNurses', 'hours', 'demand', 'minHours',
                           'maxHours', 'maxConsec', 'maxPresence']:
            if(not data.__dict__.has_key(paramName)):
                raise Exception('Parameter(%s) not contained in Configuration' % str(paramName))

        # Validate the correctness of the provided numbers
        numNurses = data.numNurses
        if(not isinstance(numNurses, (int, long)) or (numNurses <= 0)):
            raise Exception('numNurses(%s) has to be a positive integer value.' % str(numNurses))

        hours = data.hours
        if(not isinstance(hours, (int, long)) or (hours <= 0)):
            raise Exception('hours(%s) has to be a positive integer value.' % str(hours))

        if (len(data.demand)) != hours:
            raise Exception('Demand list(%s) should have same size as hours(%s).' % (str(len(data.demand)), str(hours)))

        minHours = data.minHours
        if (not isinstance(minHours, (int, long)) or (minHours <= 0)):
            raise Exception('minHours(%s) has to be a positive integer value.' % str(minHours))

        maxHours = data.maxHours
        if (not isinstance(maxHours, (int, long)) or (maxHours <= 0)):
            raise Exception('maxHours(%s) has to be a positive integer value.' % str(maxHours))

        maxConsec = data.maxConsec
        if (not isinstance(maxConsec, (int, long)) or (maxConsec <= 0)):
            raise Exception('maxConsec(%s) has to be a positive integer value.' % str(maxConsec))

        maxPresence = data.maxPresence
        if (not isinstance(maxPresence, (int, long)) or (maxPresence <= 0)):
            raise Exception('maxPresence(%s) has to be a positive integer value.' % str(maxPresence))

        if (maxHours < minHours):
            raise Exception('maxHours(%s) has to be greater or equal than minHours(%s).' % (str(maxHours), str(minHours)))

