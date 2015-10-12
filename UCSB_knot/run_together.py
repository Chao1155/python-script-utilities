#!/usr/bin/python
from multiprocessing import Pool
import os, time, subprocess

def run_bigdatabench_fs ():
    print "BigDataBench starts."
    # temp
    path = "./output/bigdatabench/"
    binary = "./build/X86/gem5.opt "
    #debug_trace = " --debug-flag=Exec --debug-file="+bench+".dtrc.gz "
    debug_trace = ""
    binary_opt = " --outdir=" + path 
    FS_config = " configs/example/fs.py --disk-image=BigDataBench-gem5.img --kernel=x86_64-vmlinux-2.6.22.9.smp "
    cpu = " -n 2 --cpu-type=detailed "
    l1 = " --caches "
    l2 = " --l2cache "
    mem = " --mem-type=SimpleMemory --mem-size=1024MB"
    script = " "
    gem5_cmd = binary + debug_trace + binary_opt + FS_config + cpu + l1 + l2 +  mem + script
    print gem5_cmd
    os.system(gem5_cmd)

def run_m5term ():
    time.sleep(5)
    cmd = "m5term localhost 3456"
    passwd = "root"
    script = "./run.sh"
    os.system(cmd)
    time.sleep(5)
    os.system(passwd)
    time.sleep(5)
    os.system(script)
    

max_subprocess = 2
p = Pool(processes=max_subprocess)
#p.apply_async(f)
p.apply_async(run_bigdatabench_fs)
p.apply_async(run_m5term)
p.close()
p.join()

#total_time = time.time() - total_time
#print "DONE: We finished all the process in %s." %str(total_time)

#from multiprocessing import Pool
#
#def f(x):
#    return x*x
#
#if __name__ == '__main__':
#    pool = Pool(processes=4)              # start 4 worker processes
#    result = pool.apply_async(f, [10])    # evaluate "f(10)" asynchronously
#    print result.get(timeout=1)           # prints "100" unless your computer is *very* slow
#    print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"
