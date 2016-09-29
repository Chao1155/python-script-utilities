import os, re
#import argparse
def clean(fileName):
	remove_keys = ['abstract', 'doi', 'isbn', 'mendeley-groups', 'keywords', 'file', 'issn']
	blind_keys = ['url']
	bibf = open(fileName, 'r')
	cleanf = open(fileName + '.tmp', 'w')
	lines = bibf.readlines()
	for line in lines:
		if re.search('^'+'|'.join(blind_keys),line):
			cleanf.write('%%%%' + line)
		elif not re.search('^'+'|'.join(remove_keys),line):
			#print line
			cleanf.write(line)
	bibf.close()
	cleanf.close()
	os.remove(fileName)
	os.rename(fileName + '.tmp', fileName)

clean('refs.bib')

