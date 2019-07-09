#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def get_a_bib(bibtex_str, debug = False):
    
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

    if debug:
        print(entry)

    return entry, end.span()[1]

def get_all_bibs(bibtex_str, debug = False):
    
    all_results = []
    unique_results = []
    c = 0

    while True:

        #get a bib entry
        entry, next_token = get_a_bib(bibtex_str, debug)
        
        #if its a valid entry
        if entry:
            
            #add entry
            all_results.append(entry)

            if entry not in unique_results:
                unique_results.append(entry)

            #do it again
            bibtex_str = bibtex_str[next_token:]

            c += 1

            if c % 10000 == 0:
                print(c)
                
        #end of the file
        else:
            break

    #after the loop
    print('All results: {}'.format(len(all_results)))
    print('Unique results: {}'.format(len(unique_results)))

    return all_results, unique_results

if __name__ == "__main__":
    
    print('I: Relax, this process can take a while..')

    #files
    target = './third_selection/old_science_direct.bib'
    bib_result =  './third_selection/new_science_direct.bib'
    
    #open the targert file
    with open(target, 'r') as f:

        #convert into string
        bibtex_str = f.read()

        #process the data
        all_bib, unique_bib = get_all_bibs(bibtex_str, False)
    
   
    #save unique bibs into a new file
    with open(bib_result, 'w') as bib_result_file:
        for bib in unique_bib:
            bib += '\n'
            bib_result_file.write(bib)
