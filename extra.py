#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import csv
import sys


"""
 simples version of some functions
"""
def get_bibtex_entry(bibtex_str, debug):
    
    #match pattern of a bibtex entry start
    regex_start = '@.*{'

    #match pattern of a bibtex entry end
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
    begin_title_regex = 'title.*= {'
    begin_year_regex  = 'year.*= {'    

    #try to find the regex patterns
    try:
        #define the data to extract
        begin_title = re.search(begin_title_regex, entry).span()[1]
        end_title   = entry.find('},', begin_title)
        
        begin_year = re.search(begin_year_regex, entry).span()[1]
        end_year   = entry.find('},', begin_year)

        begin_id = begin.span()[1]
        end_id   = entry.find(',', begin_id)

    #in case of miss something print the entry to manually analize and shutdown the execution.
    except:

        print("W: Bibtex poorly formatted, fix it and try again")
        print(entry)
        sys.exit(-1)


    #extract the date
    year     = entry[begin_year   : end_year ]
    title    = entry[begin_title  : end_title]
    paper_id = entry[begin_id : end_id]     

    results  = [title, paper_id, year, entry]
    
    #debug
    if debug:    
        
        print(entry)
        
        print("Title    : ", title)
        print("Year     : ", year)
        print("Paper id : ", paper_id)
        input()
        
        os.system('clear')

    return results, end.span()[1]


def compare_results(bibtex_files, debug):
    
    final_results = []
    final_bibtex  = ""
    
    bib_str_old = bibtex_files[0]
    bib_str_new = bibtex_files[1]
    

    #to read all the file content
    while True:
        
        #get the info about the first bib entry
        result_new, end_decision_new = get_bibtex_entry(bib_str_new, debug)
        
        #keep crawling the bibtex file
        if result_new:

            #the  new bibtex entry is in the old bibtext? check by title or ID
            if( result_new[0] in bib_str_old ):
                
                #if its true, just ignore
                pass

            #the entry is not in the old.. must be in the final
            else:

                if debug:
                    print(result_new[3])
                    input()

                final_bibtex += result_new[3]
                final_results.append(result_new) 

            #update the bibtex_strs to continue the search
            bib_str_new = bib_str_new[end_decision_new:]

        #reached the end of the files
        else:
            break
    
    #create a bibtex file and a csv file with the results
    csv_result = 'new_results.csv'
    bib_result = 'new_results.bib'
    
    with open(csv_result, 'w+', encoding="utf-8") as csv_result_file:
        csv_writer = csv.writer(csv_result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        #save
        for r in final_results:
            #write a line into the csv with the results
            csv_writer.writerow(r)

    with open(bib_result, 'w+', encoding="utf-8") as bib_result_file:
        bib_result_file.write(final_bibtex)

    #Will return nothing. Just print to inform the user
    print("Number of papers selected: {}".format(len(final_results)))
    print("I: Process finished!")