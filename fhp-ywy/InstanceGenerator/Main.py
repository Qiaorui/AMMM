import argparse, sys
from DATParser import DATParser
from ValidateConfig import ValidateConfig
from InstanceGenerator import InstanceGenerator

def run():
    argp = argparse.ArgumentParser(description='AMMM Project Instance Generator')
    argp.add_argument('configFile', help='configuration file path')
    args = argp.parse_args()

    print 'AMMM Project Instance Generator'
    print '-----------------------'
    
    print 'Reading Config file %s...' % args.configFile
    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)

    print 'Creating Instances...'
    instGen = InstanceGenerator(config)
    instGen.generate()
    
    print 'Done'

    return(0)

if __name__ == '__main__':
    sys.exit(run())
