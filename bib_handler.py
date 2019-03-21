#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import csv


def get_bibtex_entry(bibtex_str, judger):

	debug = True
	
	#match pattern of a bibtex entry start
	regex_start = '@.*{'

	#match pattern of a bibtex entry start
	regex_end   = ',.*\n}.*'
	

	#index of the next entry
	begin = re.search(regex_start, bibtex_str)
	end   = re.search(regex_end, bibtex_str)

	#there is nothing to extract (did not find the match)
	if begin is None:
		return None, 0
	if end is None:
		return None, 0

	#get the specific entry
	entry = bibtex_str[begin.span()[0] : end.span()[1] ]


	#regex to find exact position
	begin_title_regex = 'title.*= {{'
	begin_year_regex  = 'year.*= {'	
	begin_decision_regex = judger + '.*= {'

	#try to find the regex patterns
	try:
		#define the data to extract
		begin_title = re.search(begin_title_regex, entry).span()[1]
		end_title   = entry.find('}},', begin_title)
		
		begin_decision = re.search(begin_decision_regex, entry).span()[1]
		end_decision   = entry.find('},', begin_decision)
		judge_size     = len(judger)

		begin_year = re.search(begin_year_regex, entry).span()[1]
		end_year   = entry.find('},', begin_year)

		begin_id = begin.span()[1]
		end_id   = entry.find(',', begin_id)

	#in case of miss something print the entry to manually analize and shutdown the execution.
	except:

		print(entry)
		sys.exit(-1)


	#extract the date
	year     = entry[begin_year   : end_year ]
	title    = entry[begin_title  : end_title]
	decision = entry[begin_decision : end_decision]
	paper_id = entry[begin_id : end_id] 	

	results  = [title, paper_id, year, decision]
	

	#debug
	if debug:	
		
		print(entry)
		
		print("Title   : ", title)
		print("Year    : ", year)
		print("Paper id: ", paper_id)
		print("Decision: ", decision)
		#raw_input()
		
		os.system('clear')

	return results, end.span()[1]


def get_all_bibtex_entries(bibtex_str, judger, result_file):

	csv_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	while True:

		results, end_decision = get_bibtex_entry(bibtex_str, judger)

		#keep crawling the bibtex file
		if results:

			#write a line into the csv with the results
			csv_writer.writerow(results)

			#update the bibtex_str to search
			bibtex_str = bibtex_str[end_decision:]	
		
		#hit here when reach the end of the bibtex file
		else:
			break

	#return nothing since we already write the info into the csv file
	print("I: Process finished!")

if __name__ == '__main__':
	
		
	bibtex_files  = ['stevao.bib',  'misael.bib',    'domenico.bib']
	results_files = ['stevao.csv',  'misael.csv',    'domenico.csv']
	judges        = ['bytitledela', 'bytitlemisael', 'bytitledomenico']

	#refference to the position of the judgment in the lists above
	author = 2

	with open(bibtex_files[author], 'r') as f, open(results_files[author], 'w') as result_file:

		bibtex_str = f.read()
		get_all_bibtex_entries(bibtex_str, judges[author], result_file)