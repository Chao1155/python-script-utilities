#!/usr/bin/python

import sys, re

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
def read_res_csv(fileName):
    try:
        result_file = open (fileName, 'r')
    except:
        sys.exit("Cannot open csv file %s." %fileName)
    lines = result_file.readlines()
    # lines[0] is the title line.
    Index = {}
    targets = [
        'Benchmark',
        'Voltage/V',
        'Segment',
        '[Processor][Total L2s](Runtime Dynamic)',
        '[Core0][Core0](Runtime Dynamic)',
        '[BUSES0][Bus](Runtime Dynamic)',
        '[Core0][Instruction Cache](Runtime Dynamic)',
        '[Core0][Data Cache](Runtime Dynamic)',
        '[Processor][Total L2s](Subthreshold Leakage)',
        '[Processor][Total L2s](Gate Leakage)',
        '[Core0][Core0](Gate Leakage)',
        '[Core0][Core0](Subthreshold Leakage)',
        '[Core0][Instruction Cache](Gate Leakage)',
        '[Core0][Instruction Cache](Subthreshold Leakage)',
        '[Core0][Data Cache](Gate Leakage)',
        '[Core0][Data Cache](Subthreshold Leakage)', 
        '[BUSES0][Bus](Gate Leakage)',
        '[BUSES0][Bus](Subthreshold Leakage)',
    ]
    col_items = lines[0].split(',')
    for col_i in xrange(len(col_items)):
        for tag in targets:
            if tag in col_items[col_i]:
                Index[tag] = col_i
    #print Index
    L1I_1 = {}
    L1D_1 = {}
    L2 = {}
    for bench in PARSEC:
        Core1 = {}      # The dict is not efficient, try others later.
        L1I_1 = {}
        L1D_1 = {}
        BUS1 = {}
        L2 = {}
        for line in lines:
            items = line.split(',')
            #print items
            if bench in items[Index['Benchmark']] and '0.70' == items[Index['Voltage/V']]:
                Core1[int(items[Index['Segment']])] = \
                float(items[Index['[Core0][Core0](Runtime Dynamic)']]) + \
                float(items[Index['[Core0][Core0](Gate Leakage)']]) + \
                float(items[Index['[Core0][Core0](Subthreshold Leakage)']])
                L1I_1[int(items[Index['Segment']])] = \
                float(items[Index['[Core0][Instruction Cache](Runtime Dynamic)'         ]]) + \
                float(items[Index['[Core0][Instruction Cache](Gate Leakage)'            ]]) + \
                float(items[Index['[Core0][Instruction Cache](Subthreshold Leakage)'    ]])
                L1D_1[int(items[Index['Segment']])] = \
                float(items[Index['[Core0][Data Cache](Runtime Dynamic)'         ]]) + \
                float(items[Index['[Core0][Data Cache](Gate Leakage)'            ]]) + \
                float(items[Index['[Core0][Data Cache](Subthreshold Leakage)'    ]])
                BUS1[int(items[Index['Segment']])] = \
                float(items[Index['[BUSES0][Bus](Runtime Dynamic)'        ]]) + \
                float(items[Index['[BUSES0][Bus](Gate Leakage)'         ]]) + \
                float(items[Index['[BUSES0][Bus](Subthreshold Leakage)'   ]])
                L2[int(items[Index['Segment']])] = \
                float(items[Index['[Processor][Total L2s](Runtime Dynamic)' ]]) + \
                float(items[Index['[Processor][Total L2s](Subthreshold Leakage)' ]]) + \
                float(items[Index['[Processor][Total L2s](Gate Leakage)'  ]])
        #print bench, Core1, L1I_1, L1D_1, BUS1, L2
        seg_len = len(Core1)    # start from segment 2
        writef = open(bench + '_1v' + '.ptrace','w')
        # title line
        writef.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %('Core1', 'L1I_1', 'L1D_1', 'BUS1','Core2', 'L1I_2', 'L1D_2', 'BUS2', 'L2') )
        for seg in xrange(seg_len):
            #writef.write("%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n" %(Core1[seg], L1I_1[seg], L1D_1[seg], BUS1[seg], L2[seg]) )
            writef.write("%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n" %(Core1[seg + 2], L1I_1[seg + 2], L1D_1[seg + 2], BUS1[seg + 2],Core1[seg + 2], L1I_1[seg + 2], L1D_1[seg + 2], BUS1[seg + 2], L2[seg + 2]) )
        writef.close()

read_res_csv('Parsec_100us_4MB' + '/' + 'parsec_res.csv')
#read_res_csv('test.csv')

def read_all_blocks(file_dir, tags_list, file_name = "stats.txt"):
    try:
        stats_file = open (file_dir +'/'+ file_name, 'r')
    except:
        print "cannot open " + file_name + " in " + file_dir
        return;
    line_list = stats_file.readlines()
    block_counter = 0
    output_row_list = []
    #print output_row_list

    for i in range(len(line_list)):
        if ( 'Begin Simulation Statistic' in line_list[i]):
            output_row_list.append (dict([(key, '0') for key in tags_list]))
            output_row_list[block_counter]['block'] = str(block_counter)
            block_counter += 1
        for tag in tags_list:
            if ( tag in line_list[i]):
        	    output_row_list[block_counter -1 ][tag] = line_list[i].split()[1]
    stats_file.close()
    return output_row_list


def find_frequency(target):
    key  = min(frequency.keys(), key=lambda v : abs(v-target))
    return frequency[key]

def pow_2_time(l2_access, cache_leakage = 0.9, time_period = 100000, cover_ratio = 0.9, miss_penalty = 30):
    # we need all the input which should be numbers are in number format!
    # the dictionary to store the core power - frequency relation
    core_power = 0.9  # the baseline core power.
    saved_time = 0
    current_frequency = find_frequency (cache_leakage + core_power) * 1e6
    previous_frequency = find_frequency (core_power) * 1e6
    cache_gain = int(l2_access * miss_penalty * (1-cover_ratio)) # in ns
    core_gain = int(time_period * previous_frequency * (current_frequency - previous_frequency) / (current_frequency * previous_frequency))
    if core_gain > cache_gain:
        saved_time += core_gain - cache_gain
        #saved_time += core_gain
    return saved_time

#print pow_2_time (1000)
def calculate_block(data_dict_rows):
    if data_dict_rows is None:
        return
    dict_keys = list(data_dict_rows[0].keys())
    dict_rows = len(data_dict_rows)
    #print dict_keys, dict_rows
    saved_time = 0
    for row in xrange(dict_rows):
        # calculate l2 access and cpu inst per period
        if row == 0:
            data_dict_rows[row]['L2 access pp'] = '0'
            data_dict_rows[row]['N_inst pp'] = '0'
        else:
            data_dict_rows[row]['L2 access pp'] = \
            data_dict_rows[row]['system.l2.overall_accesses::total']
            data_dict_rows[row]['N_inst pp'] = \
            str ( int(data_dict_rows[row]['sim_insts']) -
                    int(data_dict_rows[row - 1]['sim_insts'])
                )
            # if the reflected miss penalty is smaller than power boosting benefit...
            saved_time += pow_2_time( int (data_dict_rows[row]['L2 access pp']))
    return saved_time

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

def analyze_files_by_all_blocks(data_dir):
    output_column_list = ['benchmark', 'size', 'block']
    output_column_list.extend(tags_list)
    # print output_column_list
    
#    try:
#    	#output_file = open ('result-1us.csv', 'w')
#    	output_file = open ('cal_stats.txt', 'w')
#    except:
#    	print "cannot open result.txt as our result."
#    	return;
    
    #print "\t".join(output_column_list)
    title_line = ''
    for item in output_column_list:
        if item in tags_dict:
            title_line += tags_dict[item] + ","
        else:
            title_line += item +','
    #output_file.write(title_line+'\n')
    for bench in PARSEC:
        for size in sizes:
			# The name here is very disappointing, try to improve it.
            file_dir = data_dir+size+"/"+bench
			#print file_dir
            output_list = read_all_blocks(file_dir,tags_list)
            time_saving = calculate_block(output_list)
            print (bench, time_saving)
            #if output_list is None:
            #    continue;
            #for i in xrange(len(output_list)):
            #    output_list[i]['benchmark'] = bench
            #    output_list[i]['size'] = size
            #    content_line = ''
            #    for key in output_column_list:
            #        content_line += output_list[i][key] + ','
            #    output_file.write(content_line+'\n')
#    output_file.close()



