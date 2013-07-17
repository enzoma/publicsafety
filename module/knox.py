#!/usr/bin/env python
# Implement the Knox test for spatio-temporal correlation

import numpy as np
import time

# This function will compute the test statistic, which is the
# number of spatio-temporally proximate data points.
def compute_test_statistic(x1, y1, t1, Nd1, x2, y2, t2, Nd2, \
                           dist_scale, time_scale, verbose=True):
  X = 0
  # Loop over all points in (x1,y1,t1)
  for d1i in range(Nd1):
    # Print out a handy status message in case the number of points
    # is extremely large and you're bored.
    if verbose and (d1i % 1000 == 0): print(d1i, Nd1)
    # Compute the number of proximate points in (x2,y2,t2)
    this = np.where(((x2-x1[d1i])*(x2-x1[d1i]) + (y2-y1[d1i])*(y2-y1[d1i]) \
                     <= dist_scale*dist_scale) & (np.abs(t2-t1[d1i]) <= \
                     time_scale))[0].size
    # Add it to the running total.
    X = X + this

  # Return the test statistic
  return X
  

# Normalize the data a bit, and then compute the Knox test statistc.
# Also compute the distribution of the test with permuted time stamps
# to assess significance.
def knox(x1, y1, t1, x2, y2, t2, dist_scale, time_scale_days, nrand=1000):
  '''Compute the Knox test statistic:
     X = # events near in space and time versus time-permuted'''

  # First get rid of points where the spatial location is undefined.
  wh1 = np.where(~np.isnan(x1))
  wh2 = np.where(~np.isnan(x2))
  x1, y1, t1 = x1[wh1], y1[wh1], t1[wh1]
  x2, y2, t2 = x2[wh2], y2[wh2], t2[wh2]

  # Now compute the times in seconds for easy math. 
  t1 = np.array([time.mktime(time.struct_time(i)) for i in t1])
  t2 = np.array([time.mktime(time.struct_time(i)) for i in t2])
  time_scale = time_scale_days * 24 * 3600

  # Determine the array sizes. We're going to be looping over (x1,y1,t1),
  # so make sure that's the shorter of the two data sets to take maximal
  # advantage of numpy's parallelization for vectorized operations.
  Nd1 = len(t1)
  Nd2 = len(t2)
  if Nd1 > Nd2:
    x3, y3, t3, Nd3 = x1, y1, t1, Nd1
    x1, y1, t1, Nd1 = x2, y2, t2, Nd2
    x2, y2, t2, Nd2 = x3, y3, t3, Nd3

  # Compute the test statistic for the real data.
  X = compute_test_statistic(x1, y1, t1, Nd1, x2, y2, t2, Nd2, \
                             dist_scale, time_scale)

  # Now compute the distribution of the test statistic by randomly
  # permuting the timestamps in one of the data sets.
  randdist = []
  for i in range(nrand):
    np.random.shuffle(t1)
    randdist.append(\
      compute_test_statistic(x1, y1, t1, Nd1, x2, y2, t2, Nd2, \
                             dist_scale, time_scale))

  # OK, we're done now.
  return X, randdist
