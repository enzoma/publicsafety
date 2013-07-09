#!/usr/bin/env python

# Import statements
import numpy as numpy
import csv

# Allow users to input csv files
# Data prereqs:
# 0) Must have column names without spaces
# 1) Must have lat/long coords
# 2) Must have timestamps (in some specific format)
# 3) Each variable must have a header

# First, query data from db or from csv to produce 
# a python (data) object.  As part of this, we identify
# the variable headers and populate the python (data) 
# object.

def importdata_from_csv(file_name):
	with open(file_name, 'rU') as f: # with avoids close at end
		r = csv.reader(f)
		header = r.next()
		columns = {} # this dictionary maps col # to name
		for columnum, columnname in enumerate(header):
			columns[columnum] = columnname
		data = {}
		for column in header:
			data[column]=[]
		for row in r:
			# for column in row, if the col name = "date",
			# then convert the column date into date format
			for key, value in enumerate(row):
				data[columns[key]].append(value)
			# column-specific processing here (date parsing et al)
			# if type(value) = string, then value.lower
	print data
	return data
	# Current problems: it's reading everything as strings
 
	
# Obtain from user aggregation level of interest
# We can aggregate based on time intervals of interest,
# based on spatial boundaries, or based on features.
# Input = original dataset; output = dataset of interest
# based on user-obtained aggregation levels.


# Perform some exploratory data analysis. 
# Exploratory functions
# a) clustering labeled data in time 
# b) proportions of labeled data in user-defined areas
# c) in vs out
# d) in vs baseline 
# e) basic univariate visualizations




