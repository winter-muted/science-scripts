#!/usr/bin/python2
import sys
import argparse
import subprocess
import os


def parse_args():
    """
    Arg parser to handle command line options.
    """
    parser = argparse.ArgumentParser(description='Get statistics on jobs run\
                    on a given queue.')
    parser.add_argument('-c',action='store_true',help='Run in collect mode.')
    parser.add_argument('-a',action='store_true',help='Run in analyze mode.')
    parser.add_argument('-q',action='store',help='Queue to collect data on.')
    parser.add_argument('-d',action='store',help='Datafile to save results.')

    opts = parser.parse_args()
    return opts

def query_queue(queue):
    """
    Get information on the jobs currently running on a given queue.
    For now, keep track of which users are running jobs, sorted by
    job count and including walltime
    """
    command = "qstat | grep " + queue
    print command
    # run the command and collect the lines returned in a list
    try:
        output = subprocess.check_output(command,shell=True)
    except:
        sys.exit("[WARN] Problem in qstat check. Likely no jobs running. Exiting.")

    jobs = {}
    for elem in output.splitlines():
        user = elem.split()[2]
        if jobs.has_key(user):
            jobs[user] += 1
        else:
            jobs[user] = 1
    # append the current system time to the dict and return
    from time import gmtime, strftime
    jobs['query_time'] = strftime("%Y-%m-%d", gmtime())

    return jobs

def store_results(results,database_file):
    """
    Store the results from a query in a database file
    """
    import sqlite3
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    try:
        cursor.execute("""Create table usage (user text, jobs integer, query_time text)""")
    except:
        pass # ignore the error for now
    payload = []
    for user in results:
        if user != 'query_time':
            payload.append([user,results[user],results['query_time']])
    cursor.executemany("Insert into usage values (?,?,?)",payload)
    conn.commit()

def get_results(date,database_file):
    """
    Get job usage on a given date
    Date resolution should be given in 1 day increments
    """
    import sqlite3
    try:
        conn = sqlite3.connect(database_file)
    except:
        sys.exit("[Error] Could not read db file.")
    cursor = conn.cursor()
    data = cursor.execute("select * from usage where query_time=(?)",[date]).fetchall()
    return data


def show_usage(date_range):
    """
    Show a summary of usage described in a database file from a time range
    Generate a bar graph of user and jobs run for different time periods
    Each user-day is an entry on the bar graph, sorted by user then day
    """
    import numpy as np
    from matplotlib import pyplot as plt
    # get the run history data for each day in range
    data = get_results("2016-04-08","data.db")
    data.sort(key=lambda tup: tup[1],reverse=True)
    N = len(data)
    # make a bar graph of usage for the two most recent weeks of usage
    fig, ax = plt.subplots()
    ind = np.arange(N)
    vals = []
    for i in range(N):
        vals.append(data[i][1])
    rect1 = ax.bar(ind,vals)
    xTickMarks = [data[i][0] for i in range(N)]
    ax.set_xticks(ind)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames,rotation=90,fontsize=12)
    

    return fig



opts = parse_args()
# results = query_queue("med16core")
# store_results(results,"data.db")
date_range = ['2016-04-01','2016-04-08']
fig = show_usage(date_range)

figures = []


fig.savefig('output.png')


# if not bool(opts.c) != bool(opts.a): #XOR
#     sys.exit("Must Specify either -c or -a")
#
# if opts.c: # collect
#     # if opts.q:
#     results = query_queue("med16core")
#     store_results(results,"data.db")
#     show_usage()

    #     try:
    #         results = query_queue(opts.q)
    #     except ValueError, Argument:
    #         results = query_queue("pmillett")
    #     except StandardError:
    #         sys.exit("[Error] Could not submit request to system.")
    # # else:
    # #     try:
    # #
    # #     except:
    # #         sys.exit("[Error] Could not submit request to system.")
    #
    # if opts.d:
    #     try:
    #         store_results(results,opts.d)
    #     except:
    #         sys.exit("[Error] Could not write to datafile.")
    # else:
    #     try:
    #         store_results(results,"usage.sql")
    #     except:
    #         sys.exit("[Error] Could not write to datafile.")

# else:      # analyze
#     try:
#         show_usage(opts.d)
#     except:
#         show_usage("usage.sql")
