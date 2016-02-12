#!/usr/bin/python2
import sys
import argparse
import glob
import subprocess

def parse_args():
    """
    The arg parser for batch submission
    """

    parser = argparse.ArgumentParser(description='\
            Submit an array of jobs to the pbs queue.  Input \
            the base name of the pbs files and the script \
            will do the rest.  Note that the regular \
            expression matcher is greedy.  Beware when similar\
            filenames exist.')
    parser.add_argument('base_name',action='store',help='Regular Expression to match (base name)' )

    opts = parser.parse_args()
    return opts


def main():
    
    opts = parse_args()
    
    filenames = []
    for file in glob.glob('*%s*.pbs' % opts.base_name):
        filenames.append(file)
    
    if len(filenames) == 0:
        sys.exit('Regular Expression Match Failed. Did you type the correct base?')

    print "Will submit the following jobs:"
    for elem in filenames:
        print elem
    selection = raw_input('Continue? [Y/N]')
    if (selection == 'Y' or selection == 'y'):
        for elem in filenames:
            try:
                subprocess.call(["qsub",elem])
                print "Submitted %s." % elem
            except:
                print "[WARN] Could not submit %s!! Check environment and filename." % elem
    else:
        print "Did not submit jobs."

if __name__ == '__main__':
    main()
