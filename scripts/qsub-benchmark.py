#!/usr/bin/python2
import os
import argparse
import sys

class qsub_benchmark(object):
    """ A collection of methods that automate the boring task
        of analyzing code scaling on a cluster.  Used to determine
        an expected scaling curve to inform runs of large batches
        of the same application.
    """

    def __init__(self,opts):
        self.base_name = opts.executable
        
        # use the provided max_nodes, or default to 8
        if int(opts.n) != 0:
            self.max_nodes = int(opts.n)
        else:
            self.max_nodes = 4
        self.ppn = 16
        
        self.mpi_cmd = "mpiexec -n"
        self.queue = "pmillett"

    def generate_pbs(self):
        print "Specify any unique runtime options here.\n" \
                "Some options are module loads and imports.\n" \
                "->"
        
        # store user pbs options line by line until blank line recieved
        header = []
        while True:
            header.append(raw_input())
            if header[-1] == "":
                header.pop()
                break

        # write pbs files to disk
        for i in range(self.ppn,(self.max_nodes+1)*self.ppn,self.ppn):
            out_file = str(i) + "-" + self.base_name
            filename = str(i) + "-" + self.base_name + ".pbs"
            
            with open(filename,"w") as f:
                f.write("#PBS -q %s\n" % (self.queue))
                f.write("#PBS -l noddes=%s:ppn=%s\n" % (i,self.ppn))
                f.write("#PBS -l walltime=1:00:00\n")
                f.write("#PBS -o %s\n" % (out_file))
                for elem in header:
                    f.write("%s\n" % elem)
                f.write("%s %s ./%s \n" % (self.mpi_cmd,i,self.base_name))

    def submit_pbs(self):
        
        # will try to import an external batch submission script
        try:
            import universe # placeholder. we all know you cant "import universe"
        except:
            # fall back to this quick and dirty implementation
            # warn of this!
            # inform the user of the jobs to be submitted
            print "[WARN]external submission lib failed import, on fallback!"
            print "Will submit the following jobs to queue %s:" % self.queue
            for i in range(self.ppn,(self.max_nodes+1)*self.ppn,self.ppn):
                print "%s-%s.pbs" % (i,self.base_name)
            a = raw_input("Continue? [Y/N]")
            if (a == 'y' or a == 'Y' or a == 'yes' or a == 'Yes'):
                print "Submitted jobs."
            else:
                print "Did not submit jobs."
    
    def plot_results(self):
        pass


def parse_args():
    """ 
    Implemented here is the argument parser.  The help interface is
    automatically produced by the argparser library
    """

    parser = argparse.ArgumentParser(description='\
            Generates an array of jobs using the given executable and times \
            their execution.  The current implementation simply adds a node \
            up to 16 nodes (half the cluster), aligned to the n=16 procs \
            per node on the pmillett queue. You can override this behavior \
            with -n.  When analyzing the results, ensure \
            all the runs have completed before generating the results.')
    parser.add_argument('-g',action='store_true',help='generate and submit scaling runs')
    parser.add_argument('-p',action='store_true',help='plot results of a scaling run')
    parser.add_argument('-s',action='store_true',help='supress dumb term plot output')
    parser.add_argument('-n',action='store',help='max number of nodes to use')
    parser.add_argument('executable',action='store')

    opts = parser.parse_args()
    return opts

def main():
    opts = parse_args()
    handle = qsub_benchmark(opts)

    if opts.g:
        handle.generate_pbs()
        handle.submit_pbs()
    elif opts.p:
        handle.plot_results()
    else:
        sys.exit('Specify either generate(g) or plot(p).')
    
if __name__ == '__main__':
    main()
