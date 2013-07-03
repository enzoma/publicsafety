#!/usr/bin/env python

import csv
#STATION,DATE,DLY-TMAX-NORMAL,DLY-TMAX-STDDEV,DLY-TMIN-NORMAL,DLY-TMIN-STDDEV

def ftoc(f):
  return (f - 32.0) * 5.0/9.0

with open('/mnt/data1/CPD/ord_climate.csv','r') as f_in,\
     open('/mnt/data1/CPD/ord_climate_parsed.csv','w') as f_out:
  csvreader  = csv.reader(f_in)
  csvwriter  = csv.writer(f_out)
  in_header  = csvreader.next()
  out_header = ['Date', 'T_min (C)', 'T_max (C)', 'T_min_std (C)', \
                'T_max_std (C)']
  csvwriter.writerow(out_header)
  data       = []
  for row in csvreader:
    datestr = row[1]
    date = datestr[4:6]+'/'+datestr[6:]+'/'+datestr[0:4]
    # TMIN and TMAX are in tenths of deg C
    tmin     = ftoc(float(row[in_header.index('DLY-TMIN-NORMAL')])/10.0)
    tmax     = ftoc(float(row[in_header.index('DLY-TMAX-NORMAL')])/10.0)
    tmin_std = 5.0/9.0*(float(row[in_header.index('DLY-TMIN-STDDEV')])/10.0)
    tmax_std = 5.0/9.0*(float(row[in_header.index('DLY-TMAX-STDDEV')])/10.0)

    csvwriter.writerow([date,tmin,tmax,tmin_std,tmax_std])
