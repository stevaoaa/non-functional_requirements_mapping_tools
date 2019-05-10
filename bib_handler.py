#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import csv


"""
	given a bib, find the bibtex_token then add the token_to_be_added and return the new_bib
"""
def add_token_to_bib(bib, bib_token, token_to_be_added):
	new_bib = ""

	start_token = bib.find(bib_token)
	end_token = bib[start_token:].find("},")
		
	if start_token == -1:
		print("W: Invalid token. Exiting")
		sys.exit(-1)
	else:
		
		index = start_token + end_token

		new_bib = bib[: index + 2]
		new_bib = new_bib + token_to_be_added	
		new_bib = new_bib + bib[index + 2:]

	return new_bib

def get_bibtex_entry(bibtex_str, judger, debug):
	
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

	results  = [title, paper_id, year, entry, decision]
	

	#debug
	if debug:	
		
		print(entry)
		
		print("Title    : ", title)
		print("Year     : ", year)
		print("Paper id : ", paper_id)
		print("Decision : ", decision)
		raw_input()
		
		os.system('clear')

	return results, end.span()[1]


def get_all_bibtex_entries(bibtex_str, judger, result_file, debug):

	csv_writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	while True:

		results, end_decision = get_bibtex_entry(bibtex_str, judger, debug)

		#keep crawling the bibtex file
		if results:
			
			#remove the bibtex from the results before save into csv (dont need all the bibtex info into the csv file)
			results.pop(-2)

			#write a line into the csv with the results
			csv_writer.writerow(results)

			#update the bibtex_str to search
			bibtex_str = bibtex_str[end_decision:]	
		
		#hit here when reach the end of the bibtex file
		else:
			break

	#return nothing since we already write the info into the csv file
	print("I: Process finished!")


def merge_results(bibtex_files, judges, debug):
	
	final_results = []
	final_bibtex  = ""
	
	bib_str_a = bibtex_files[0]
	bib_str_b = bibtex_files[1]
	bib_str_c = bibtex_files[2]
	
	#to read all the file content
	while True:
		
		#get the info about the first bib entry
		result_a, end_decision_a = get_bibtex_entry(bib_str_a, judges[0], debug)
		result_b, end_decision_b = get_bibtex_entry(bib_str_b, judges[1], debug)
		result_c, end_decision_c = get_bibtex_entry(bib_str_c, judges[2], debug)
		
		#keep crawling the bibtex file
		if result_a:

			#is the same bibtex entry?
			if((result_a[0] == result_b[0]) & (result_a[0] == result_c[0])):
				
				#count the judgment
				judgment = [result_a[-1], result_b[-1], result_c[-1]]
				
				#check the judgment
				if debug:
					print("Stevao:   {}".format(judgment[0]))
					print("Misael:   {}".format(judgment[1]))
					print("Domenico: {}".format(judgment[2]))
					raw_input()


				#get one bib and merge the results
				one_bib = result_c.pop(-2)
				bib_token = "bytitledomenico = "
				token_to_be_added = "\n  bytitlemisael = {{{}}},\n  bytitledela = {{{}}},".format(judgment[0], judgment[1])

				#merge the results into one_bib
				one_bib = add_token_to_bib(one_bib, bib_token, token_to_be_added)					

				#decisions
				no    = judgment.count('no')
				yes   = judgment.count('yes')
				doubt = judgment.count('doubt')

				#rule to aprove the papers
				if no < 2:
					
					#extract the bibtex from the results before save results into the list that will turn the csv file
					final_bibtex += '\n\n' + one_bib

					#save the results into the final list
					final_results.append(result_c)


			#the entries are not the same
			else:
				print("W: The bibtex files need to be equally ordered!")
				sys.exit(-1)

			#update the bibtex_strs to continue the search
			bib_str_a = bib_str_a[end_decision_a:]
			bib_str_b = bib_str_b[end_decision_b:]
			bib_str_c = bib_str_c[end_decision_c:]

		#reached the end of the files
		else:
			break
	

	#create a bibtex file and a csv file with the results
	csv_result = 'final.csv'
	bib_result = 'final.bib'
	

	with open(csv_result, 'w+') as csv_result_file:
		csv_writer = csv.writer(csv_result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		#save
		for r in final_results:
			#write a line into the csv with the results
			csv_writer.writerow(r)

	with open(bib_result, 'w+') as bib_result_file:
		bib_result_file.write(final_bibtex)

	#Will return nothing. Just print to inform the user
	print("Number of papers selected: {}".format(len(final_results)))
	print("I: Process finished!")



def menu():

	#initialize to avoid 'referenced before assignment'
	option = author = debug = None

	#possible methods
	print("1 - Create CSV from a bib file")
	print("2 - Merge resuts according to selection criteria")	

	#read the option
	option = int(input("Chose an method: "))
	
	#execute according to the option
	if option not in [1, 2]:
		print("W: Invalid option!")
		sys.exit(-1)


	#only selects author for 1 option
	if option == 1:

		#refference to the position of the judgment in the lists above
		print("0 - Stevao")
		print("1 - Misael")
		print("2 - Domenico")			

		#read the author
		author = int(input("Chose an author: "))

		if author not in [0, 1, 2]:
			print("W: Invalid author!")
			sys.exit(-1)

	#get all files/dirs from the root
	dirs_list = os.listdir(os.getcwd())

	#filter only valid dirs
	dirs = [d for d in dirs_list if (os.path.isdir(d)) & ('.' not in d)]

	#automatic generate the options
	for i in range(len(dirs)):
		print("{} - {}".format(i, dirs[i]))

	#read the dir
	target_dir = int(input("Chose the targeted dir: "))

	#validate
	if target_dir not in range(len(dirs)):
		print("W: Invalid directory!")
		sys.exit(-1)

	#change to target dir
	os.chdir(dirs[target_dir])


	#debug
	print("0 - No")
	print("1 - Yes")

	#read the option
	debug = int(input("Wanna debug the operation?: "))

	if debug not in [0, 1]:
		print("W: Invalid debug value!")
		sys.exit(-1)


	return option, author, debug




if __name__ == '__main__':

	#files
	bibtex_files  = ['stevao.bib',  'misael.bib',    'domenico.bib']
	results_files = ['stevao.csv',  'misael.csv',    'domenico.csv']
	judges        = ['bytitledela', 'bytitlemisael', 'bytitledomenico']

	#get inputs from user
	option, author, debug = menu()

	if option == 1:

		with open(bibtex_files[author], 'r') as f, open(results_files[author], 'w') as result_file:

			bibtex_str = f.read()
			get_all_bibtex_entries(bibtex_str, judges[author], result_file, debug)

	if option == 2:

		with open(bibtex_files[0], 'r') as bib_0, open(bibtex_files[1], 'r') as bib_1, open(bibtex_files[2], 'r') as bib_2:

			#convert the files into string and add to a list
			bibs = [bib_0.read(), bib_1.read(), bib_2.read()]

			#build the merged result
			merge_results(bibs, judges, debug)