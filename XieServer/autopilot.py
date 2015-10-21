#!/usr/bin/python2.7
from multiprocessing import Pool
import os, time, random, subprocess, socket
import argparse # for command line options

# parameters initialization
Gem5Root = os.path.abspath('./gem5-stable')
#Gem5Root = os.path.abspath('./gem5-dev')
max_subprocess = 64

PARSEC = [
    'blackscholes', 
    'bodytrack', 
    'canneal', 
    'dedup', 
    'facesim',      
    #'ferret', 
    'fluidanimate', 
    'freqmine', 
    #'rtview',
    'streamcluster',
    'swaptions', 
    'vips', 
    'x264', 
]

#SIZE = ['2','4', '16', '32', '64', '128', '192']
SIZE = ['4']

def generate_parsec_fs_scripts(core_number):
    global Gem5Root
    global PARSEC
    os.chdir("./configs/parsec")
    for bench in PARSEC:
        subprocess.call(["./writescripts.pl", bench, str(core_number)])
        print "Generating script for " + bench + " in " + str(core_number) + " mode."
    os.chdir(Gem5Root)

def build_gem5(build_option, gem5type):
        os.system ("scons build/%s/gem5.%s -j4" %(build_option, gem5type))

# the run command for PARSEC fs configurations.
# You can change the configuration in this function, or take this as an example.
def run_parsec_fs (root, bench, size):
    num_cpus = '1'
    generate_parsec_fs_scripts(int(num_cpus))
    assoc = '4'
    if int(size) <=64:
        assoc = '8'
    elif int(size) <= 128:
        assoc = '16'
    elif int(size) <= 192:
        assoc = '24'
    path = root + bench
    binary = "./build/X86/gem5.fast "
    #debug_trace = " --debug-flag=Exec --debug-file="+bench+".dtrc.gz "
    debug_trace = ""
    binary_opt = " --outdir=" + path 
    FS_config = " configs/myconfigs/fs.py --disk-image=x86root-parsec.img --kernel=x86_64-vmlinux-2.6.22.9.smp "
    cpu = " -n " + num_cpus + " --cpu-type=detailed --cpu-clock=2000MHz --sys-clock=1000MHz "
    l1 = " --caches --l1i_size=32kB --l1d_size=32kB --l1i_assoc=2 --l1d_assoc=2 "
    l2 = " --l2cache --l2_size="+size+"MB"+" --l2_assoc="+assoc + " --l2monitor "
    mem = " --mem-type=SimpleMemory --mem-size=2048MB"
    #script = " --script=configs/parsec/" + bench + "_" + num_cpus + "c_simlarge.rcS "
    script = " --script=configs/parsec/" + bench + "_" + num_cpus + "c_simmedium.rcS -r1"
    #script = " --script=configs/boot/hack_back_ckpt.rcS "

    log = " | tee " + path +"/log.txt"
    gem5_cmd = binary + debug_trace + binary_opt + FS_config + cpu + l1 + l2 +  mem + script + log
    #print gem5_cmd
    time.sleep(random.random())
    os.system(gem5_cmd)

def run_bigdatabench_fs ():
    num_cpus = '1'
    size = '4'
    assoc = '16'
    path = "./output/bigdatabench"
    binary = "./build/X86/gem5.fast "
    #debug_trace = " --debug-flag=Exec --debug-file="+bench+".dtrc.gz "
    debug_trace = ""
    binary_opt = " --outdir=" + path 
    #FS_config = " configs/myconfigs/fs.py --disk-image=BigDataBench-gem5.img --kernel=vmlinux-22-22-64 "
    FS_config = " configs/myconfigs/fs.py --disk-image=BigDataBench-gem5.img --kernel=x86_64-vmlinux-2.6.22.9.smp "
    cpu = " -n " + num_cpus + " --cpu-type=detailed --cpu-clock=2000MHz --sys-clock=1000MHz "
    l1 = " --caches --l1i_size=32kB --l1d_size=32kB --l1i_assoc=2 --l1d_assoc=2 "
    l2 = " --l2cache --l2_size="+size+"MB"+" --l2_assoc="+assoc
    mem = " --mem-type=SimpleMemory --mem-size=2048MB"
    script = " --script=./config/bigdatabench/test.rcS"
    log = " | tee " + path +"/log.txt"
    gem5_cmd = binary + debug_trace + binary_opt + FS_config + cpu + l1 + l2 +  mem + script + log
    #print gem5_cmd
    time.sleep(random.random())
    os.system(gem5_cmd)

def fs_empty_run (root):
    path = root
    binary = "./build/ALPHA/gem5.fast "
    binary_opt = " --outdir=" + path 
    FS_config = " configs/myconfigs/fs.py "
    cpu = " -n 4 --cpu-type=detailed --cpu-clock=2000MHz --sys-clock=1000MHz "
    l1 = " --caches --l1i_size=32kB --l1d_size=32kB --l1i_assoc=2 --l1d_assoc=2 "
    l2 = " --l2cache --l2_size=4MB --l2_assoc=16 "
    mem = " --mem-type=SimpleMemory --mem-size=512MB"
    script = " --script=configs/parsec/empty_os.rcS "
    gem5_cmd = binary + binary_opt + FS_config + cpu + l1 + l2 +  mem + script
    os.system(gem5_cmd)

def run_spec_se (root, bench, cache_size):
    path = root + bench
    binary = "./build/ALPHA/gem5.fast "
    binary_opt = " --outdir=" + path 
    FS_config = " configs/myconfigs/se_spec.py "
    cpu = " -n 1 --cpu-type=detailed --cpu-clock=2000MHz --sys-clock=1000MHz -F 100000000 -I 1000000000 "
    l1 = " --caches --l1i_size=32kB --l1d_size=32kB --l1i_assoc=2 --l1d_assoc=2 "
    l2 = " --l2cache --l2_size=" + cache_size + "kB --l2_assoc=8 "
    #l3 = " --l3cache --l3_size=8MB --l3_assoc=16 "
    mem = " --mem-type=SimpleMemory --mem-size=512MB"
    benchmark = " --bench=" + bench
    #gem5_cmd = binary + binary_opt + FS_config + cpu + l1 + l2 + l3 +  mem + benchmark
    gem5_cmd = binary + binary_opt + FS_config + cpu + l1 + l2  +  mem + benchmark
    #print gem5_cmd
    time.sleep(random.random())
    os.system(gem5_cmd)

def usr_admit(MAX_PROCESSES, total_p):
    print "We have ", MAX_PROCESSES, "virtual cores,and ", total_p, "processes to go."
    while(1):
        user_input = raw_input("Shall we start? (y/n)\n")
        if user_input == 'n':
            return False
        elif user_input == 'y':
            return True

def check_dir(path):
    # hack the dir temperaly.
    if not os.path.exists(path):
        os.mkdir(path)

def benchmark_iteration(output_dir, benchmark_set, iteration_run):
    global max_subprocess
    p = Pool(max_subprocess)

    #if not usr_admit(max_subprocess, len(benchmark_set) * len(SIZE)):
    #    print "Exit the simulation due to user abandon."
    #    exit(1)
    print "The simulation STARTS!\nYou can detach the tmux now."
    total_time = time.time()
    for bench in benchmark_set:
        for size in SIZE:
            time.sleep( 1 + random.random())
            p.apply_async(iteration_run, (output_dir + "Parsec_dist_"+size+"MB/", bench, size))
    p.close()
    p.join()
    total_time = time.time() - total_time
    print "DONE: We finished all the process in %s." %str(total_time)

def set_environment_variables():
    #PATHS FOR DEPENDENCIES NEEDED TO BUILD/RUN GEM5
    deps_path = ":/home/chao/gem5" # improve later.
    #Set swig path dependencies (communication between python and c++)
    os.environ["PATH"] += deps_path + "/swig-3.0/swig-3.0.5/bin"
    #Set gcc path dependencies (require 4.9.2 for our build)
    os.environ["LD_LIBRARY_PATH"] = deps_path + "/gcc-4.9.2/gcc-4.9.2/lib64"
    os.environ["PATH"] += deps_path + "/gcc-4.9.2/gcc-4.9.2/bin"
    #Set python path dependencies (require version 2.6.9 for our build)
    os.environ["PATH"] += deps_path + "/python-2.6/Python-2.6.9/bin"
    #Set protobuf path dependencies
    os.environ["PKG_CONFIG_PATH"] = deps_path + "/protobuf-2.6/protobuf-2.6.0/lib/pkgconfig"
    #export LD_LIBRARY_PATH :=${LD_LIBRARY_PATH}:$(deps_path)/protobuf-2.6/protobuf-2.6.0/lib
    os.environ["LD_LIBRARY_PATH"] += deps_path + "/protobuf-2.6/protobuf-2.6.0/lib"
    #Set mercurial path
    os.environ["PATH"] += deps_path + "/mercurial-3.3/mercurial-3.3/bin"
    #Set m5term
    os.environ["PATH"] += ":/home/chaozhang/bin"
    
    # debug in case
    #print os.environ["PATH"]
    #print ""

def run_m5term ():
    ip_str = os.popen("ip addr show | grep 192").read()
    ip_addr = ip_str.split()[1][:-3]
    print "The IP address is " + ip_addr

    cmd = "m5term " + ip_addr + " 3456"
    passwd = "root"
    script = "./run.sh"
    time.sleep(60)
    os.system(cmd)
    time.sleep(1800)
    os.system(passwd)
    time.sleep(60)
    os.system(script)

def decode_trace():
    os.system('pwd')
    for bench in PARSEC:
        path = './output/Parsec_dist_4MB'
        in_cmd = path +'/' +bench + '/l2bus2l2.ptr.gz'
        out_cmd = path +'/' +bench + '/trace_l2bus2l2.txt'
        os.system('./decode_packet_trace.py ' + in_cmd + " " + out_cmd)
        #print './decode_packet_trace.py ' + in_cmd + " " + out_cmd

# the configuraion for this simulation slot.
if __name__=='__main__':
    # uncomment this if you want to send me a mail when simulation finishes.
#    output_root_dir = "./output/SPEC-l2-256K/"
    os.chdir(Gem5Root)
    output_root_dir = "./output/"
    check_dir(output_root_dir)
    build_gem5("X86", "fast")
   # build_gem5("ALPHA", "opt")
    # The run command for all iterations.
    #benchmark_iteration(output_root_dir, SPEC2006, run_spec_se)
    #benchmark_iteration(output_root_dir, PARSEC, run_parsec_fs)

    parser = argparse.ArgumentParser(description='Auto execution script for gem5.')
    parser.add_argument('bench', metavar='BENCHMARK_INDEX', 
        type=int, nargs=1, help = '0 for parsec, 1 for bigdata, 2 for decode')
    args=parser.parse_args()
    set_environment_variables()
    if args.bench[0] == 0:
        benchmark_iteration(output_root_dir, PARSEC, run_parsec_fs)
    elif args.bench[0] == 1:
        max_subprocess = 2
        p = Pool(processes=max_subprocess)
        p.apply_async(run_bigdatabench_fs)
        run_bigdatabench_fs()
        p.apply_async(run_m5term)
        p.close()
        p.join()
    elif args.bench[0] == 2:
        decode_trace()
    else:
        print "Wrong arguments. EXIT."
        exit(1)
        
