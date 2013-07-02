#!/usr/bin/env python

import csv

with open('/mnt/data1/CPD/ord_weather.csv','r') as f_in,\
     open('/mnt/data1/CPD/ord_weather_parsed.csv','w') as f_out:
  csvreader  = csv.reader(f_in)
  csvwriter  = csv.writer(f_out)
  in_header  = csvreader.next()
  out_header = ['Date', 'T_min (C)', 'T_max (C)', 'Precipitation (mm)', \
                'Snowfall (mm)', 'Avg wind (m/s)']
  csvwriter.writerow(out_header)
  data       = []
  for row in csvreader:
    datestr = row[1]
    date = datestr[4:6]+'/'+datestr[6:]+'/'+datestr[0:4]
    # TMIN and TMAX are in tenths of deg C
    tmin = float(row[in_header.index('TMIN')])/10.0
    tmax = float(row[in_header.index('TMAX')])/10.0
    # PRCP is in tenths of mm
    prcp = float(row[in_header.index('PRCP')])/10.0
    # SNOW is in mm
    snow = float(row[in_header.index('SNOW')])
    # AWND is in tenths of m/s
    awnd = float(row[in_header.index('AWND')])/10.0

    csvwriter.writerow([date,tmin,tmax,prcp,snow,awnd])
