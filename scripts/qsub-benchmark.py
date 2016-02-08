import os

class qsub_benchmark(object):
    """ A collection of methods that automate the boring task
        of analyzing code scaling on a cluster.  Used to determine
        an expected scaling curve to inform runs of large batches
        of the same application.
    """

    def __init__(self):
        self.base_name = 'jobs'
        self.num_jobs = 3


    def generate_pbs(self):
        pass


    def submit_pbs(self):

        # inform the user of the jobs to be submitted
        print "Will submit the following jobs:"
        for i in range(self.num_jobs):
            print "%s%s.pbs" % (self.base_name,i)
        a = raw_input("Continue? [Y/N]")
        if (a == 'y' or a == 'Y' or a == 'yes' or a == 'Yes'):
            print "Submitted jobs."
        else:
            print "Did not submit jobs."

    def plot_results(self):
        pass


handle = qsub_benchmark()
handle.submit_pbs()
