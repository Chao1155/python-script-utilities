#!/usr/bin/python
tags_list = ['sim_seconds', 
	'host_seconds', 
	'system.l2.overall_accesses::total',
	'system.l2.overall_miss_rate::total',
    'system.l2.tags.tagsinuse',
	'icache.overall_accesses::total', 
	'dcache.overall_accesses::total']
tags_list_output_forms={
    'sim_seconds': 'S_time (s)',
	'host_seconds': 'H_time (s)', 
	'system.l2.overall_accesses::total':'L2 access',
	'system.l2.overall_miss_rate::total': 'L2 miss rate',
    'system.l2.tags.tagsinuse': 'L2 touched',
	'icache.overall_accesses::total': 'L1I access', 
	'dcache.overall_accesses::total': 'L1D access'
}
PARSEC = [
    'blackscholes', 
    'bodytrack', 
    'canneal', 
    'dedup', 
    'facesim',      
    'ferret', 
    'fluidanimate', 
    'freqmine', 
    'rtview',
    'streamcluster',
    'swaptions', 
    'vips', 
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
    
    try:
    	output_file = open ('result-100us.csv', 'w')
    	#output_file = open ('result.txt', 'w')
    except:
    	print "cannot open result.txt as our result."
    	return;
    
    #print "\t".join(output_column_list)
    title_line = ''
    for item in output_column_list:
        if item in tags_list_output_forms:
            title_line += tags_list_output_forms[item] + ","
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


