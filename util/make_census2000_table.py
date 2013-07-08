#!/usr/bin/env python
import census
import csv

# Read the 2000 decadal census data using Tom's census code.
c = census.census(2000)
c10 = census.census(2010)
c.aggregate_to_10()

# Open up a CSV file for the output.
with open(census.datadir + 'census2000_tract_population.csv','w') as f:
  cwriter = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
  # Loop through tracts and write tract FIPS number, total population,
  # and geometry.
  for tract, data in c10.data.iteritems():
    pop_tot=None
    if tract in c.data10.keys(): pop_tot=c.data10[tract]['POP_TOT']
    row = [tract, pop_tot, 'SRID=3435; '+data['geo'].ExportToWkt()]
    # Write out the tract to the CSV file.
    cwriter.writerow(row)
