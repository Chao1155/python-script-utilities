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
    'rtview',
    'streamcluster',
    'swaptions', 
    'vips', 
    'x264', 
]
sizes=['4MB']#, '128MB','192MB']
	#file_dir = "/Users/ShuiHan/Yue_Parsec_64MB/canneal"

def read_all_blocks(file_dir, tags_list, bundle = 1, file_name = "stats.txt"):
    """ works as the main block of analyze function.
    """
    try:
        stats_file = open (file_dir +'/'+ file_name, 'r')
    except:
        print "cannot open " + file_name + " in " + file_dir
        return;
    line_list = stats_file.readlines()
    block_counter = 0
    output_row_list = []
    #print output_row_list

    # bund the stats of 'bundle' periods together.
    bundle_remain = bundle 
    for i in range(len(line_list)):
    # for each line do the following check
        if ( 'Begin Simulation Statistic' in line_list[i]):
            if bundle_remain == bundle:
                output_row_list.append (dict([(key, 0) for key in tags_list]))
                output_row_list[block_counter]['block'] = str(block_counter)
                block_counter += 1
                
        for tag in tags_list:
            if ( tag in line_list[i]):
        	    output_row_list[block_counter -1 ][tag] += float(line_list[i].split()[1])
        if ( 'End Simulation Statistic' in line_list[i]):
            bundle_remain -=1
            if bundle_remain == 0:
                bundle_remain = bundle
            
    stats_file.close()
    return output_row_list

def analyze_files_by_all_blocks(data_dir):
    output_column_list = ['benchmark', 'size', 'block']
    output_column_list.extend(tags_list)
    # print output_column_list
    
    try:
    	output_file = open ('result-10us.csv', 'w')
    	#output_file = open ('result.txt', 'w')
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
            output_list = read_all_blocks(file_dir,tags_list, 10)
            if output_list is None:
                continue;
            for i in xrange(len(output_list)):
                output_list[i]['benchmark'] = bench
                output_list[i]['size'] = size
                content_line = ''
                #print output_list[i]
                for key in output_column_list:
                    content_line += str(output_list[i][key]) + ','
                output_file.write(content_line+'\n')
    output_file.close()

#analyze_files("/Users/ShuiHan/Yue_Parsec_")
#analyze_files_by_all_blocks("./Parsec_100us_")
analyze_files_by_all_blocks("./Parsec_1us_")


