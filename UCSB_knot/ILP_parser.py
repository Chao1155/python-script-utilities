#!/usr/bin/python

# parse the data into a dictionary.
#from multidata import *
from data import *

# technique no.1
# convert the power benefit to time.
#def trade_power_for_frequency(l2_access, optimal = False, cache_leakage = 0.9, time_period = 100000, cover_ratio = 0.9, miss_penalty = 30): # for single core
def trade_power_for_frequency(l2_access, delta_inst, optimal = False, cache_leakage = 1.59, time_period = 100000, cover_ratio = 0.9, miss_penalty = 30): # for 4 cores
    # we need all the input which should be numbers are in number format!
    # the dictionary to store the core power - frequency relation
    core_power = 0.9  # the baseline core power.
    saved_time = 0
    current_frequency = find_frequency (cache_leakage + core_power) * 1e6
    previous_frequency = find_frequency (core_power) * 1e6
    cache_gain = int(l2_access * miss_penalty * (1-cover_ratio)) # in ns
    core_gain = int(time_period * previous_frequency * (current_frequency - previous_frequency) / (current_frequency * previous_frequency))
    max_core_gain = delta_inst * 1e9/ previous_frequency     # the increasement should not be faster than other cores.
    if optimal:
        saved_time += core_gain
    else:
        if core_gain > cache_gain:
            saved_time += core_gain - cache_gain
        if saved_time > max_core_gain:
            saved_time = max_core_gain
    return saved_time       # in nano second scale
# technique no.2
# convert IO to the performance.
def IO_throttle(IO_pins, access, miss_rate):
    req_size = 64 # byte
    freq_io = 1e-9
    t_mem = 30e-9 # s
    cycle_one_io = (req_size * 8 / IO_pins)
    cycle_all_io = cycle_one_io * access * miss_rate
    t_all = cycle_all_io * freq_io + access * miss_rate* t_mem 
    # memory access latency lower than l1.
    return t_all * 0.1
# technique no. 3
# find the benefit intervals
def pick_for_dvfs(l2_access, cache_leakage = 1.59, time_period = 100000, cover_ratio = 0.9, miss_penalty = 30):
    core_power = 0.9  # the baseline core power.
    current_frequency = find_frequency (cache_leakage + core_power) * 1e6
    previous_frequency = find_frequency (core_power) * 1e6
    cache_gain = int(l2_access * miss_penalty * (1-cover_ratio)) # in ns
    core_gain = int(time_period * previous_frequency * (current_frequency - previous_frequency) / (current_frequency * previous_frequency))
    if cache_gain == 0:
        return 0
    else:
        return 1

# get the gains for cache.
def gains_for_cache(cache_access, hit_lat = 5, miss_penalty = 20):
    alpha = 0.1
    cache_gain = int(cache_access * alpha * (miss_penalty - hit_lat)) # in ns
    return cache_gain
# get the gains for cores
def gains_for_core(insts, inst_cycle = 1.0, slow_f = 1.0e9, fast_f = 1.1e9):
    coeff = slow_f * (1/slow_f - 1/fast_f)
    core_gain = int(insts * inst_cycle/slow_f * 1e9 * coeff) # in ns
    return core_gain
# get all gains by each period
def get_gains_1c(data_dict_rows, row):
    g_l2 = gains_for_cache(int(data_dict_rows[row]['system.l2.overall_accesses::total']), 5, 15)
    g_core = gains_for_core(int(data_dict_rows[row]['system.switch_cpus.fetch.Insts']))
    return g_core, g_l2
        
# overall output program
def run(data_dir):
    try:
    	#output_file = open ('IO_throttle.txt', 'w')
    	#output_file = open ('trade_power_4c.txt', 'w')
    	output_file = open ('gains_traces_parsec_1c.txt', 'w')
    except:
    	print "cannot open result.txt as our result."
    	return;
    print_table = []
    for bench in PARSEC:
		# The name here is very disappointing, try to improve it.
        file_dir = data_dir+"/"+bench
		#print file_dir
        output_list = read_all_blocks(file_dir,tags_list)
        #data_dict_rows = polish_blocks(output_list)
        data_dict_rows = output_list
        speed_inst = 0
        for row in xrange(len(data_dict_rows)):
            # calculate l2 access and cpu inst per period
            if row != 0:
                (g_core, g_cache) = get_gains_1c(data_dict_rows, row)
                print >> output_file, bench, row, g_core, g_cache
    output_file.close()
run("./Parsec_100us_4MB")

# format of the gain trace:
# bench, row, g_core, g_cache


