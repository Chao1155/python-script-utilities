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
def pick_for_sb(l2_access, cache_leakage = 1.59, time_period = 100000, cover_ratio = 0.9, miss_penalty = 30):
    core_power = 0.9  # the baseline core power.
    current_frequency = find_frequency (cache_leakage + core_power) * 1e6
    previous_frequency = find_frequency (core_power) * 1e6
    cache_gain = int(l2_access * miss_penalty * (1-cover_ratio)) # in ns
    core_gain = int(time_period * previous_frequency * (current_frequency - previous_frequency) / (current_frequency * previous_frequency))
    if core_gain >= cache_gain:
        return 1
    else:
        return 0
# overall output program
def run(data_dir):
    try:
    	#output_file = open ('IO_throttle.txt', 'w')
    	#output_file = open ('trade_power_4c.txt', 'w')
    	output_file = open ('sb_period_decisions.txt', 'w')
    except:
    	print "cannot open result.txt as our result."
    	return;
    for bench in PARSEC:
		# The name here is very disappointing, try to improve it.
        file_dir = data_dir+"/"+bench
		#print file_dir
        output_list = read_all_blocks(file_dir,tags_list)
        #data_dict_rows = polish_blocks(output_list)
        data_dict_rows = output_list
        speed_inst = 0
        total_inst = 0
        saved_time = 0
        speed_cores = [0,0,0,0]
        execution_time = {32:0, 33:0, 40:0, 41:0, 48:0, 49:0, 56:0, 57:0, 64:0, 65:0, 72:0, 73:0, 80:0, 81:0}
        total_time = 100000 * (len(data_dict_rows) -1)
        for row in xrange(len(data_dict_rows)):
            # calculate l2 access and cpu inst per period
            if row != 0:
                # if the reflected miss penalty is smaller than power boosting benefit...
#                (core, most_inst, second_inst, total) = select_busiest (data_dict_rows[row], 4)
#                speed_inst += most_inst
#                speed_cores[core] += 1
#                total_inst += total
                cache_access = int (data_dict_rows[row]['system.l2.overall_accesses::total'])
#                saved_time += trade_power_for_frequency(cache_access, most_inst - second_inst)
                print pick_for_sb (cache_access)
                #for pins in range(32, 81, 8):
                #    execution_time[pins] += IO_throttle(pins, int (data_dict_rows[row]['L2 access pp']), float (data_dict_rows[row]['system.l2.overall_miss_rate::total'])) + \
                #    int(data_dict_rows[row]['N_inst pp']) * 0.5e-9
                #    execution_time[pins+1] += IO_throttle(pins, int (data_dict_rows[row]['L2 access pp']), 1) + \
                #    int(data_dict_rows[row]['N_inst pp']) * 0.5e-9
        #print >>output_file, bench, execution_time[32], execution_time[40], execution_time[48], execution_time[56], execution_time[64], execution_time[72], execution_time[80], execution_time[33], execution_time[41], execution_time[49], execution_time[57], execution_time[65], execution_time[73], execution_time[81]
#        print >> output_file, bench, float(saved_time)/total_time, float(speed_inst) / (total_inst), speed_cores
    output_file.close()
run("./Parsec_100us_16MBl3")


def analyze_files_by_one_block(data_dir):
	output_column_list = ['benchmark', 'size']
	output_column_list.extend(tags_list)
	# print output_column_list

	output_column_dict = dict([(key, '0') for key in output_column_list])

	try:
		output_file = open ('result.txt', 'w')
	except:
		print "cannot open result.txt as our result."
		return;

	#print "\t".join(output_column_list)
	title_line = "\t".join(output_column_list)
	output_file.write(title_line+'\n')
	for bench in PARSEC:
		for size in sizes:
			# The name here is very disappointing, try to improve it.
			file_dir = data_dir+size+"/"+bench
			#print file_dir
			read_one_block(file_dir,tags_list, output_column_dict, 3)
			output_column_dict['benchmark'] = bench
			output_column_dict['size'] = size
			# print "\t".join(output_column_dict.values())
			content_line = ''
			for key in output_column_list:
				content_line += output_column_dict[key] + '\t'
			#print content_line
			output_file.write(content_line+'\n')

	output_file.close()

