#!/usr/bin/python

tags_dict = {}

def add_dict_entry(key, output = "", diction = tags_dict):
    if output == "":
        output = key
    try:
        diction [key] = output
    except:
        print "something wrong at 2 lines above."

add_dict_entry('sim_seconds',                          'S_time (s)'        )
add_dict_entry('host_seconds',                         'H_time (s)'        )
add_dict_entry('sim_insts',                            'N_inst'            )
add_dict_entry('sim_ops',                              'N_ops'             )
add_dict_entry('icache.overall_accesses::total',       'L1I access'        )
add_dict_entry('dcache.overall_accesses::total',       'L1D access'        )
add_dict_entry('system.l2.overall_accesses::total',    'L2 access'         )
add_dict_entry('system.l2.overall_miss_rate::total',   'L2 miss rate'      )
add_dict_entry('system.l2.tags.tagsinuse',             'L2 used lines'     )
add_dict_entry('system.l2.tags.replacements',          'L2 replaces'       )
add_dict_entry('system.l2.tags.total_refs',            'L2 refs_valid'     )
add_dict_entry('cpu.icache.overall_miss_rate::total',  'L1I miss rate'     )
add_dict_entry('cpu.dcache.overall_miss_rate::total',  'L1D miss rate'     )


tags_list = list(tags_dict.keys())

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
sizes=['4MB']#, '128MB','192MB']
	#file_dir = "/Users/ShuiHan/Yue_Parsec_64MB/canneal"

frequency = {}
add_dict_entry(  0.26,1000   ,frequency)
add_dict_entry(  0.29,1010   ,frequency)
add_dict_entry(  0.32,1020   ,frequency)
add_dict_entry(  0.35,1030   ,frequency)
add_dict_entry(  0.38,1040   ,frequency)
add_dict_entry(  0.42,1050   ,frequency)
add_dict_entry(  0.46,1060   ,frequency)
add_dict_entry(  0.50,1070   ,frequency)
add_dict_entry(  0.55,1080   ,frequency)
add_dict_entry(  0.59,1090   ,frequency)
add_dict_entry(  0.64,1100   ,frequency)
add_dict_entry(  0.69,1110   ,frequency)
add_dict_entry(  0.75,1120   ,frequency)
add_dict_entry(  0.80,1130   ,frequency)
add_dict_entry(  0.86,1140   ,frequency)
add_dict_entry(  0.93,1150  ,frequency)
add_dict_entry(  0.99,1160  ,frequency)
add_dict_entry(  1.06,1170  ,frequency)
add_dict_entry(  1.13,1180  ,frequency)
add_dict_entry(  1.20,1190  ,frequency)
add_dict_entry(  1.28,1200  ,frequency)
add_dict_entry(  1.36,1210  ,frequency)
add_dict_entry(  1.45,1220  ,frequency)
add_dict_entry(  1.53,1230  ,frequency)
add_dict_entry(  1.62,1240  ,frequency)
add_dict_entry(  1.72,1250  ,frequency)
add_dict_entry(  1.81,1260  ,frequency)
add_dict_entry(  1.91,1270  ,frequency)
add_dict_entry(  2.02,1280  ,frequency)
add_dict_entry(  2.13,1290  ,frequency)
add_dict_entry(  2.24,1300  ,frequency)
add_dict_entry(  2.36,1310  ,frequency)
add_dict_entry(  2.48,1320  ,frequency)
add_dict_entry(  2.60,1330  ,frequency)
add_dict_entry(  2.73,1340  ,frequency)
add_dict_entry(  2.87,1350  ,frequency)
add_dict_entry(  3.00,1360  ,frequency)
add_dict_entry(  3.15,1370  ,frequency)
add_dict_entry(  3.29,1380  ,frequency)
add_dict_entry(  3.45,1390  ,frequency)
add_dict_entry(  3.60,1400  ,frequency)
add_dict_entry(  3.76,1410  ,frequency)
add_dict_entry(  3.93,1420  ,frequency)
add_dict_entry(  4.10,1430  ,frequency)
add_dict_entry(  4.28,1440  ,frequency)
add_dict_entry(  4.46,1450  ,frequency)
add_dict_entry(  4.65,1460  ,frequency)
add_dict_entry(  4.85,1470  ,frequency)
add_dict_entry(  5.05,1480  ,frequency)
add_dict_entry(  5.25,1490  ,frequency)
add_dict_entry(  5.47,1500  ,frequency)
add_dict_entry(  5.69,1510  ,frequency)
add_dict_entry(  5.91,1520  ,frequency)
add_dict_entry(  6.14,1530  ,frequency)
add_dict_entry(  6.38,1540  ,frequency)
add_dict_entry(  6.62,1550  ,frequency)
add_dict_entry(  6.88,1560  ,frequency)
add_dict_entry(  7.13,1570  ,frequency)
add_dict_entry(  7.40,1580  ,frequency)
add_dict_entry(  7.67,1590  ,frequency)
add_dict_entry(  7.95,1600  ,frequency)
add_dict_entry(  8.24,1610  ,frequency)
add_dict_entry(  8.54,1620  ,frequency)
add_dict_entry(  8.84,1630  ,frequency)
add_dict_entry(  9.15,1640  ,frequency)
add_dict_entry(  9.47,1650  ,frequency)
add_dict_entry(  9.80,1660  ,frequency)
add_dict_entry(  10.14,1670 ,frequency)
add_dict_entry(  10.48,1680 ,frequency)
add_dict_entry(  10.84,1690 ,frequency)
add_dict_entry(  11.20,1700 ,frequency)
add_dict_entry(  11.57,1710 ,frequency)
add_dict_entry(  11.95,1720 ,frequency)
add_dict_entry(  12.35,1730 ,frequency)
add_dict_entry(  12.75,1740 ,frequency)
add_dict_entry(  13.16,1750 ,frequency)
add_dict_entry(  13.58,1760 ,frequency)
add_dict_entry(  14.01,1770 ,frequency)
add_dict_entry(  14.45,1780 ,frequency)
add_dict_entry(  14.90,1790 ,frequency)
add_dict_entry(  15.36,1800 ,frequency)
add_dict_entry(  15.84,1810 ,frequency)
add_dict_entry(  16.32,1820 ,frequency)
add_dict_entry(  16.81,1830 ,frequency)
add_dict_entry(  17.32,1840 ,frequency)
add_dict_entry(  17.84,1850 ,frequency)
add_dict_entry(  18.37,1860 ,frequency)
add_dict_entry(  18.91,1870 ,frequency)
add_dict_entry(  19.47,1880 ,frequency)
add_dict_entry(  20.03,1890 ,frequency)
add_dict_entry(  20.61,1900 ,frequency)
add_dict_entry(  21.20,1910 ,frequency)
add_dict_entry(  21.81,1920 ,frequency)
add_dict_entry(  22.43,1930 ,frequency)
add_dict_entry(  23.06,1940 ,frequency)
add_dict_entry(  23.70,1950 ,frequency)
add_dict_entry(  24.36,1960 ,frequency)
add_dict_entry(  25.04,1970 ,frequency)
add_dict_entry(  25.72,1980 ,frequency)
add_dict_entry(  26.43,1990 ,frequency)
add_dict_entry(  27.14,2000 ,frequency)
def read_one_block(file_dir, tags_list, tags_value_dict, 
	block_index = 3, file_name = "stats.txt"):
	try:
		stats_file = open (file_dir +'/'+ file_name, 'r')
	except:
		print "cannot open " + file_name + " in " + file_dir
		return;

	line_list = stats_file.readlines()
	
	block_counter = 0		# only fetch the data in # th block.

	for i in range(len(line_list)):
		if ( 'Begin Simulation Statistic' in line_list[i]):
			block_counter += 1
		if block_counter == block_index:
			for tag in tags_list:
				if ( tag in line_list[i]):
				#print line_list[i]
				# get the number which is the second and put into the dict.
					tags_value_dict[tag] = line_list[i].split()[1]

	stats_file.close()

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
            print ("%s, %d, %.2f" % (bench, time_saving, float(time_saving) / 9000000))
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

analyze_files_by_all_blocks("./Parsec_100us_")


