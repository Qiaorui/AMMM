import os, random, shutil

# Generate instances based on read configuration. 
class InstanceGenerator(object):
    def __init__(self, config):
        self.config = config
    
    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        minHoursCanGenerate = self.config.minHoursCanGenerate
        maxHoursCanGenerate = self.config.maxHoursCanGenerate


        if(not os.path.isdir(instancesDirectory)):
            #raise Exception('Directory(%s) does not exist' % instancesDirectory)
            os.makedirs(instancesDirectory)
        else:
            for the_file in os.listdir(instancesDirectory):
                file_path = os.path.join(instancesDirectory, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                        # elif os.path.isdir(file_path): shutil.rmtree(file_path)
                except Exception as e:
                    print(e)

        for i in xrange(0, numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            hours = random.randint(minHoursCanGenerate, maxHoursCanGenerate)
            numNurses = int(hours * random.uniform(1.5, 3))
            demand = [int(hours/2*random.random()) for i in range(hours)]
            maxHours = random.randint(max(2, hours//3.5) , hours//2)
            minHours = random.randint(1, maxHours)
            maxConsec = random.randint(2, maxHours)
            maxPresence = random.randint(maxHours, min(hours, maxHours * 2 - 1))

            # Write to the .dat file
            fInstance.write('numNurses = %d;\n' % numNurses)
            fInstance.write('hours = %d;\n' % hours)
            # translate vector of floats into vector of strings and concatenate that strings separating them by a single space character
            fInstance.write('demand = [%s];\n' % (' '.join(map(str, demand))))

            fInstance.write('minHours = %d;\n' % minHours)
            fInstance.write('maxHours = %d;\n' % maxHours)
            fInstance.write('maxConsec = %d;\n' % maxConsec)
            fInstance.write('maxPresence = %d;\n' % maxPresence)

            fInstance.close()
