#!/usr/bin/python
import sys
import os


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
    f.write('#PBS -l nodes=1:ppn=1 \n')
    f.write('#PBS -l walltime=20:00:00 \n')
    f.write('#PBS -M chao@ece.ucsb.edu\n')
    f.write('#PBS -m e\n')
    f.write('#PBS -j oe\n')
    f.write('#PBS -o /home/chaozhang/batch_tasks/output\n')
    f.write('echo "Job started on `hostname` at `date`"\n')
    f.write('cd /home/chaozhang/gem5/gem5-10436\n')
    f.write('pwd\n')
    f.write('./set_env.sh\n')
    f.write('\n')

def creat_task(f, bench_name):
    f.write('./autopilot.py -m 0 -b ' + bench_name + '\n')

def creat_end(f):
    f.write('echo "Job Ended at `date`"')
    f.write('echo "Have a good day!"')
    f.write('echo " "')

def run_pbs(script):
    os.system ('qsub -q long ' + script)

# generate the PBS head section, including how many resources ul use.
task_id = 0
for bench in PARSEC:
    task_id += 1
    job_name = './jobs/parsec_' + str(task_id) + '.job'
    outfile = open (job_name, 'w')
    print "creating job for " + job_name
    creat_head(outfile)
    creat_task(outfile, bench)
    creat_end(outfile)
    outfile.close()
    run_pbs(job_name)
