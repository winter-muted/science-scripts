#!/usr/bin/python2
import os
import argparse
import sys
import re

# from subprocess import call,Popen,communicate
import subprocess

class qsub_benchmark(object):
    """ A collection of methods that automate the boring task
        of analyzing code scaling on a cluster.  Used to determine
        an expected scaling curve to inform runs of large batches
        of the same application.
    """

    def __init__(self,opts):

        # use the provided max_nodes, or default to 8
        if opts.n is None:
            self.max_nodes = 16
        else:
            self.max_nodes = int(opts.n)
        self.ppn = 16

        self.mpi_cmd = "mpiexec -n"
        self.queue = "pmillett"
        

        # do alll this nasty string stuff
        self.base_name = opts.executable
        self.plot_output = self.base_name + '.jpg'
        self.data_output = self.base_name + '.data'
        self.generate_interal_file_lists()

    def generate_interal_file_lists(self):
        self.pbs_filenames = []
        self.data_filenames = []
        for i in range(self.ppn,(self.max_nodes+1)*self.ppn,self.ppn):
            pbs_file = str(i) + '-' + self.base_name + '.pbs'
            data_file = str(i) + '-' + self.base_name + '.data'
            self.pbs_filenames.append(pbs_file)
            self.data_filenames.append(data_file)

    def generate_pbs(self):
        print "Specify any unique runtime options here.\n" \
                "Some options are module loads and imports.\n"


        # store user pbs options line by line until blank line recieved
        header = []
        while True:
            header.append(raw_input("> "))
            if header[-1] == "":
                header.pop()
                break

        # write pbs files to disk
        for i,filename in enumerate(self.pbs_filenames):
            with open(filename,"w") as f:
                f.write("#PBS -q %s\n" % (self.queue))
                f.write("#PBS -l nodes=%s:ppn=%s\n" % (i+1,self.ppn))
                f.write("#PBS -l walltime=1:00:00\n")
                f.write("#PBS -o %s\n" % (self.data_filenames[i]))
                for elem in header:
                    f.write("%s\n" % elem)
                f.write("%s %s ./%s \n" % (self.mpi_cmd,(i+1)*self.ppn,self.base_name))

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

            a = raw_input("Continue? [Y/N] ")
            if (a == 'y' or a == 'Y' or a == 'yes' or a == 'Yes'):
                for file in self.pbs_filenames: # interate over the pbs files
                    try:
                        subprocess.call(["qsub",str(file)])
                    except:
                        sys.exit("[ERR]qsub failure. are you in a job scheduling environment?")
                print "[Submitted]"
            else:   # don't submit now
                print "Did not submit jobs."

    def plot_results(self,opts):

        # Complicated but safe-ish reading of results
        walltimes = [0] * self.max_nodes
        for i, file in enumerate(self.data_filenames):
            try:
                f = open(file,'r')
            except:
                print "[WARN] Could not open %s" % (file)
            while True:
                line = f.readline()
                if not line: break
                expr = re.match('Resources Used:.*',line)
                if expr:
                    walltimes[i] =  expr.group(0).partition('walltime=')[-1]
        
        formatted_walltimes = [0] * self.max_nodes
        for i, elem in enumerate(walltimes):
           try:
                days,hours,minutes = walltimes[i].split(':')
                formatted_walltimes[i] = str(int(days)*3600 + int(hours)*60 + int(minutes))
           except:
                pass
        # print results into a file for later usage
        with open(self.data_output,'w') as f:
            for i,elem in enumerate(formatted_walltimes):
                f.write("%s %s\n" % (self.ppn*(i+1),formatted_walltimes[i]))

        plot_call = ("set title 'No. threads vs. walltime'\n"
                   "set xlabel 'No. threads'\n"
                   "set ylabel 'Log Walltime (s)'\n"
                   #"set logscale y\n"
                   "set term jpeg size 1024,768\n"
                   "set output '%s'\n"
                   "plot '%s' using 1:2 lt 1 pt 4 ps 2 with linespoints"
                    % (self.plot_output,self.data_output))

        with open("plot.gp",'w') as f:
            f.write(plot_call)
        os.system('gnuplot plot.gp')
        os.remove('plot.gp')
        
        if not opts.s: # dumb term output
            plot_call = ("set title 'No. threads vs. walltime'\n"
                        "set xlabel 'No. threads'\n"
                        "set ylabel 'Log Walltime (s)'\n"
                       # "set logscale y\n"
                       # "set term jpeg size 1024,768\n"
                       # "set output '%s'\n"
                        "set term dumb\n"
                        "plot '%s' using 1:2 lt 1 pt 4 ps 2 with linespoints"
                       # % (self.plot_output,self.data_output))
                        %(self.data_output))

            with open("plot.gp",'w') as f:
                f.write(plot_call)
            os.system('gnuplot plot.gp')
            os.remove('plot.gp')
         


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
        handle.plot_results(opts)
    else:
        sys.exit('Specify either generate(g) or plot(p).')

if __name__ == '__main__':
    main()
