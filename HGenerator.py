#!/usr/bin/python

'''
HGenerator is a tool that allows generating .h files with currency pair names, symbols and instrument IDs
Uses a .csv file as input
CSV format: 'ccy, reverse, comment, extra'
Written by ArtemF
Version 1.1
Copyright (C) 2018 Fluent Trade Technologies
'''

import re
import csv
import sys
import os
import os.path

# customize output file names here
out_names = 'pair_names.h'
out_symbols = 'pair_symbols.h'
out_ins_ids = 'instrument_ids.h'

def show_help():
    print("\nScript usage: %s <path_to_csv_file>\n" % sys.argv[0])

if len(sys.argv[1:]) == 0:
	show_help()
	exit()

# checks if input file exists
if not os.path.isfile(sys.argv[1]):
	print '\nNo such input file: {}\n'.format(sys.argv[1])
	exit()

# removes files if they already exist
if os.path.isfile('./' + out_names): 
	os.remove('./' + out_names)
if os.path.isfile('./' + out_symbols):
	os.remove('./' + out_symbols)
if os.path.isfile('./' + out_ins_ids):
	os.remove('./' + out_ins_ids)

# the counter below is used for enum in instrument_id.h
enum_counter = 0

def headers():
	names_file.write('const char * currency_pair_names[] = {\n\t\"NONE\"\n')
	symbols_file.write('char const * const ccypair::symbols[] = {\n')
	ins_ids_file.write('enum INSTRUMENT_ID\n{\n\tINSTR_NON_CODE = -1,\n')

def generate_names_line(ccy):
	names_file.write('\t"{}_{}",'.format(ccy[:-3], ccy[-3:]) + '\n')

def generate_symbols_line(ccy):
	symbols_file.write('\t"{}/{}",'.format(ccy[:-3], ccy[-3:]).upper() + '\n')

def generate_ins_ids_line(ccy, rev, comment, extra):
	global enum_counter
	prefix = ''
	append_comment = ''
	if re.match('y|Y|yes|YES|Yes', extra):
		prefix = 'EXTRA_'
	if comment != '':
		append_comment = " // "+comment
	ins_ids_file.write('\t{}INSTR_{} = {},'.format(prefix, ccy, enum_counter).upper() + append_comment + '\n')
	enum_counter += 1
	if re.match('y|Y|yes|YES|Yes', rev):
		rev_ccy = ccy[-3:] + ccy[:-3]
		ins_ids_file.write('\t{}INSTR_{} = {}INSTR_{},'.format(prefix, rev_ccy, prefix, ccy).upper() + '\n')

def footers():
	names_file.write('\tNULL\n};\n')
	symbols_file.write('\tNULL\n};\n')
	ins_ids_file.write('\t// watermark for matrix.\n\tINSTR_CONTROLLER_SIZE,\n\tINSTR_ACCOUNT = INSTR_CONTROLLER_SIZE + 0,\n\tINSTR_GROSS = INSTR_CONTROLLER_SIZE + 1,\n\tINSTR_NET = INSTR_CONTROLLER_SIZE + 2,\n\tINSTR_TOTAL_BUY = INSTR_CONTROLLER_SIZE + 3,\n\tINSTR_TOTAL_SELL = INSTR_CONTROLLER_SIZE + 4,\n\tINSTR_SIZE\n};\n')

if __name__ == "__main__":
	with open(sys.argv[1]) as infile, \
	open(out_names, 'a') as names_file, \
	open(out_symbols, 'a') as symbols_file, \
	open(out_ins_ids, 'a') as ins_ids_file:
        	next(infile, None)        #skips 1st line with column names
	        rows = csv.reader(infile)
		headers()
		for row in rows:
			ccy = ''.join(re.findall('[A-Za-z]+', row[0])).lower()
			generate_names_line(ccy)
			generate_symbols_line(ccy)
			generate_ins_ids_line(ccy, row[1], row[2], row[3])
		footers()
	print '\n\tDONE: .h files have been generated\n'

