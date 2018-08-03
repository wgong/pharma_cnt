#!/usr/bin/env python
# -*- coding: UTF-8-*-

import getopt, sys
import os.path
import codecs
import time
import re

# use nested dict as main data structure
# key= drug name, value= {person:cost} dict
drug_map = {}  

err_lines = []  # store bad data line
header_line = "" 
header_map = {} # index column name
num_lines = 0

def usage():
    print("")
    print("Usage:")
    print("  To count pharma in a file")
    print("    python " + sys.argv[0] + ' -i <input.txt> -o <output.txt>')
    print("")
    sys.exit(1)

def remove_comma_in_quotes(s):
    return re.sub(r'(?!(([^"]*"){2})*[^"]*$),', '', s)
    
def write_output(file_out):
    #print(drug_map)
    cost_map = {}
    for drug_name in drug_map.keys():
        person_map = drug_map[drug_name]
        total_cost = 0
        num_person = 0
        for full_name in person_map.keys():
            num_person = num_person + 1
            total_cost = total_cost + person_map[full_name]
            
        cost_map["%s,%d" % (drug_name, num_person)] = total_cost

    with open(file_out,'w') as f:
        f.write("drug_name,num_prescriber,total_cost")
        for k in sorted(cost_map, key=cost_map.get, reverse=True):           
            f.write("\n%s,%f" % (k, cost_map[k])) 


def write_err(file_err):
    if len(err_lines):
        with open(file_err,'w') as f:
            f.write(header_line)
            for i in err_lines:
                f.write('\n' + i)    

def process_data(file_in):
    global header_line, num_lines
    with open(file_in,'r') as f:
        for line in iter(f.readline,''):
            if num_lines < 1:
                # first line must be header
                # ID,PRESCRIBER_LAST_NAME,PRESCRIBER_FIRST_NAME,DRUG_NAME,DRUG_COST
                # process header column names
                header_line=line.strip()
                headers=header_line.split(',')
                ih = 0
                for h in headers:
                    header_map[h.strip().upper()] = ih
                    ih = ih+1
                
            else:
                line=line.strip().upper()
                # skip blank / comment line
                if len(line) < 1 or line[0] == '#':
                    continue
                    
                # skip error data line
                cols = remove_comma_in_quotes(line).split(',')
                if len(cols) != len(headers):
                    err_lines.append(line)
                    continue

                try:
                    drug_cost = float(cols[header_map['DRUG_COST']].strip())
                except ValueError:
                    err_lines.append(line)
                    continue

                # parse data element
                full_name = cols[header_map['PRESCRIBER_LAST_NAME']].strip() + ':' \
                            + cols[header_map['PRESCRIBER_FIRST_NAME']].strip()
                drug_name = cols[header_map['DRUG_NAME']].strip()
                
                # validate drug name
                if len(drug_name) < 1:
                    err_lines.append(line)
                    continue

                # populate nested dict
                if drug_name in drug_map:
                    person_map = drug_map[drug_name]
                    if full_name in person_map:
                        # accumulate cost for the same person
                        person_map[full_name] = person_map[full_name] + drug_cost
                    else:
                        person_map[full_name] = drug_cost
                else:
                    person_map = {full_name : drug_cost}
                    
                drug_map[drug_name] = person_map
            
            num_lines = num_lines + 1
    
def main():
    # parse param
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=","output="])
    except getopt.GetoptError as err:
        print("[%s] %s" %(sys.argv[0],str(err))) 
        usage()
        
    file_in = ""
    file_out = ""
    
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-i", "--input"):
            file_in = a
        elif o in ("-o", "--output"):
            file_out = a
        else:
            assert False, "unknown option"
            
    if file_in == "" or not os.path.exists(file_in):
        print("[%s] Invalid input file!" % (sys.argv[0],))
        sys.exit(1)
    else:
        # test read
        try:       
            f = codecs.open(file_in,mode='r',encoding=sys.getfilesystemencoding())
        except IOError:
            print("[%s] Unable to read input file!" % (sys.argv[0],))
            usage()
        else:
            f.close()
    

    if file_out == "":
        print("[%s] Missing output file!" % (sys.argv[0],))
        sys.exit(1)

    head, tail = os.path.split(file_out)
    file_err = os.path.join(head, tail.split('.')[0] + ".err")

    ts1 = time.clock()
    # start processing
    process_data(file_in)

    #print(header_line)

    # write result
    write_output(file_out)
    write_err(file_err)
    
    ts2 = time.clock()
    
    print("Processed %d lines in %f sec" % (num_lines, (ts2-ts1) ))
    
    # exit
    sys.exit(0)
  
if __name__ == "__main__":
    main()