#!/usr/bin/env python
import census
import csv

# Read the 2010 decadal census data using Tom's census code.
c = census.census(2010)

# Open up a CSV file for the output.
with open(census.datadir + 'census2010_tract_population.csv','w') as f:
  cwriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
  # Loop through tracts and write tract FIPS number, total population,
  # and geometry.
  for tract, data in c.data.iteritems():
    row = [tract, data['POP_TOT'], 'SRID=3435; '+data['geo'].ExportToWkt()]
    # Write out the tract to the CSV file.
    cwriter.writerow(row)
