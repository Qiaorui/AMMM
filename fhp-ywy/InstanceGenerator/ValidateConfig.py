# Validate config attributes read from a DAT file.
class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances',
                           'minHoursCanGenerate', 'maxHoursCanGenerate']:
            if(not data.__dict__.has_key(paramName)):
                raise Exception('Parameter(%s) not contained in Configuration' % str(paramName))

        # Validate instance file's directory, prefix and extension are provided
        instancesDirectory = data.instancesDirectory
        if(len(instancesDirectory) == 0): raise Exception('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if(len(fileNamePrefix) == 0): raise Exception('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if(len(fileNameExtension) == 0): raise Exception('Value for fileNameExtension is empty')

        # Validate the correctness of the provided number of instances to generate
        numInstances = data.numInstances
        if(not isinstance(numInstances, (int, long)) or (numInstances <= 0)):
            raise Exception('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        minHoursCanGenerate = data.minHoursCanGenerate
        if(not isinstance(minHoursCanGenerate, (int, long)) or (minHoursCanGenerate <= 0)):
            raise Exception('minHoursCanGenerate(%s) has to be a positive integer value.' % str(minHoursCanGenerate))

        maxHoursCanGenerate = data.maxHoursCanGenerate
        if (not isinstance(maxHoursCanGenerate, (int, long)) or (maxHoursCanGenerate <= 0)):
            raise Exception('maxHoursCanGenerate(%s) has to be a positive integer value.' % str(maxHoursCanGenerate))

        if (maxHoursCanGenerate < minHoursCanGenerate):
            raise Exception('maxHoursCanGenerate(%s) has to be greater or equal than minHoursCanGenerate(%s).' % (str(maxHoursCanGenerate), str(minHoursCanGenerate)))