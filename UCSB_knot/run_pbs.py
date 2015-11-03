#!/usr/bin/python
import sys
import os
import re


PARSEC = [
    'blackscholes', 
    'bodytrack', 
    'canneal', 
    'dedup', 
    'facesim',      
    'ferret', 
    'fluidanimate', 
    'freqmine', 
    #'rtview',
    'streamcluster',
    'swaptions', 
    #'vips', 
    'x264', 
]

def creat_head(f):
    f.write('#!/bin/bash\n')
    f.write('\n')
    f.write('#PBS -l nodes=1:ppn=1 \n')     # reduce resource requirement to get priority.
    f.write('#PBS -l walltime=20:00:00 \n') # gem5 longer than 1 day is useless.
    f.write('#PBS -M chao@ece.ucsb.edu\n')  # send you an email, if you require.
    f.write('#PBS -m a\n')          # 'a' is abort, 'e' is end
    f.write('#PBS -j oe\n')
    f.write('#PBS -o /home/chaozhang/batch_tasks/output\n') # PBS output locations, named by <jobname>.o<jobid>
    f.write('echo "Job started on `hostname` at `date`"\n')
    f.write('cd /home/chaozhang/gem5/gem5-10436\n')
    f.write('pwd\n')
    f.write('./set_env.sh\n')
    f.write('\n')

def creat_task(f, bench_name):
    f.write('./autopilot.py -m 0 -b ' + bench_name + '\n')

def creat_end(f):
    f.write('echo "Job Ended at `date`"\n')
    f.write('echo "Have a good day!"\n')
    f.write('echo " "\n')

def run_pbs(script):
    #os.system ('qsub -q long ' + script)
    results = os.popen ('qsub -q long ' + script).read().split()[0] # get the first word return
    id_str = re.search('(\d+)',results).group(0) # the number befor dot.
    return id_str

# generate the PBS head section, including how many resources ul use.
task_id = 0
task_list = {}
probe_file = open('launched_jobs.txt', 'w')
for bench in PARSEC:
    task_id += 1
    job_name = './jobs/parsec_' + str(task_id) + '.job'     # the name must be unique for dict!
    outfile = open (job_name, 'w')
    #print "creating job script for " + job_name
    creat_head(outfile)
    creat_task(outfile, bench)
    creat_end(outfile)
    outfile.close()
    job_id = run_pbs(job_name)
    print "launched job %s with PID %s." %(job_name, job_id)
    task_list[job_name] = job_id
    probe_file.write(job_id + '\n')
probe_file.close()
print "All the jobs are launched. (stored in lauched_jobs.txt)"

