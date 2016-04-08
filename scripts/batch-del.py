#!/usr/bin/python2
import sys
import argparse
import subprocess
import os
import re
def parse_args():
    """
    Arg parser to handle command line options.
    """
    parser = argparse.ArgumentParser(description='\
                Delete an array of jobs using regular expressions.')
    parser.add_argument('-a',action='store_true',help='Delete all jobs currenly running for your user')

    parser.add_argument('-r',action='store',help='Regular expression of job description to match')

    opts = parser.parse_args()
    return opts


def del_job(job):
    """
    A function to delete a single pbs job.  Takes as input
    the job name to be deleted.
    """
    try:
        subprocess.call(['qdel'],str(job['id']))
        print "Deleted job %s" % job['id']
    except:
        print "Something bad happened when deleting job %s." % job['id']

def get_running_jobs():
    """
    Get a list of currently running jobs and their desciriptions
    """
    user = os.environ['USER']
    try:
        ret = subprocess.check_output(["qstat","-u %s" % user])
    except:
        sys.exit("Problem with qstat command.")

    if not ret:
        sys.exit("There are no jobs currently running for user.")

    ret = ret.split('\n')

    for i in range(5): # delete the first lines as junk
        ret.pop(0)
    ret.pop() # delete the final newline

    jobs = []
    for elem in ret:
        job = {
                'id' : elem.split()[0].strip('.sched'),
                'name' : elem.split()[3]
              }
        jobs.append(job)
    return jobs


def parse_regex(jobs,regex):
    """
    Match a regex to a list of strings in jobs
    """

    # loop through each job and try to match regex
    matches = []
    for job in jobs:
        if re.match(regex,job['name']):
            matches.append(job)
            print "[RE] Matched %s (%s)" % (job['name'],job['id'])

    return matches


def main():
    opts = parse_args()

    # build the job list
    jobs = get_running_jobs()

    # decide which jobs to terminate

    if opts.a: # delete all running jobs
        print "[DEL] Deleting all currently running jobs."
        for job in jobs:
            del_job(job)

    else: # match the regex and delete those instead
        print "[DEL] Deleting jobs matching regex"
        matches = parse_regex(jobs,opts.r)
        if not matches:
            sys.exit("No jobs matched the regular expression.")
        cont = raw_input("Are you sure you want to delete? (Y/N)")
        if (cont == 'Y' or cont == 'y'):
            for job in matches:
                del_job(job)


if __name__ == '__main__':
    main()
