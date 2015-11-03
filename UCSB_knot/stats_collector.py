#!/usr/bin/python

tags_dict = {}

def add_search_item(key, output = "", diction = tags_dict):
    if output == "":
        output = key
    try:
        diction [key] = output
    except:
        print "something wrong at 2 lines above."

add_search_item('sim_seconds',                          'S_time (s)'        )
add_search_item('host_seconds',                         'H_time (s)'        )
add_search_item('sim_insts',                            'N_inst'            )
add_search_item('sim_ops',                              'N_ops'             )
add_search_item('icache.overall_accesses::total',       'L1I access'        )
add_search_item('dcache.overall_accesses::total',       'L1D access'        )
add_search_item('system.l2.overall_accesses::total',    'L2 access'         )
add_search_item('system.l2.overall_miss_rate::total',   'L2 miss rate'      )
add_search_item('system.l2.tags.tagsinuse',             'L2 used lines'     )
add_search_item('system.l2.tags.replacements',          'L2 replaces'       )
add_search_item('system.l2.tags.total_refs',            'L2 refs_valid'     )
add_search_item('cpu.icache.overall_miss_rate::total',  'L1I miss rate'     )
add_search_item('cpu.dcache.overall_miss_rate::total',  'L1D miss rate'     )


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
    output_column_list = ['benchmark', 'size', 'block', 'L2 access pp', 'N_inst pp']
    output_column_list.extend(tags_list)
    # print output_column_list
    
    try:
    	output_file = open ('result-100us-W2.csv', 'w')
    except:
    	print "cannot open result.txt as our result."
    	return;
    
    #print "\t".join(output_column_list)
    title_line = ''
    for item in output_column_list:
        if item in tags_dict:
            title_line += tags_dict[item] + ","
        else:
            title_line += item +','
    output_file.write(title_line+'\n')
    for bench in PARSEC:
        for size in sizes:
			# The name here is very disappointing, try to improve it.
            file_dir = data_dir+size+"/"+bench
			#print file_dir
            output_list = read_all_blocks(file_dir,tags_list)
            if output_list is None:
                continue;
            calculate_block(output_list)
            for i in xrange(len(output_list)):
                output_list[i]['benchmark'] = bench
                output_list[i]['size'] = size
                content_line = ''
                for key in output_column_list:
                    content_line += output_list[i][key] + ','
                output_file.write(content_line+'\n')
    output_file.close()

#analyze_files("/Users/ShuiHan/Yue_Parsec_")
analyze_files_by_all_blocks("./Parsec_100us_")


