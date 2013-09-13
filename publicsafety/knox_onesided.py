#!/usr/bin/env python
# Implement the Knox test for spatio-temporal correlation

import numpy as np
import time, copy

# This function will compute the test statistic, which is the
# number of spatio-temporally proximate data points.
def compute_test_statistic(x1, y1, t1, Nd1, x2, y2, t2, Nd2, \
                           dist_scale, time_scale, verbose=True, nrand=1000, t1leads=True):

  t1prime = copy.deepcopy(t1)
  randtimes = []
  for i in range(nrand):
    np.random.shuffle(t1prime)
    randtimes.append(copy.deepcopy(t1prime))

  X = 0
  randX = np.zeros(nrand)
  # Loop over all points in (x1,y1,t1)
  for d1i in range(Nd1):
    # Print out a handy status message in case the number of points
    # is extremely large and you're bored.
    if verbose and (d1i % 1000 == 0): print(d1i, Nd1)
    # Compute the number of space-proximate points in (x2,y2)
    this_dist = np.where(((x2-x1[d1i])*(x2-x1[d1i]) + (y2-y1[d1i])*(y2-y1[d1i]) \
                          <= dist_scale*dist_scale))
    # Now compute the time-proximate points from t2 for real data.
    this=0
    if t1leads:
      this = np.where((t2[this_dist] > t1[d1i]) & (t2[this_dist]-t1[d1i] <= time_scale))[0].size
    else:
      this = np.where((t2[this_dist] < t1[d1i]) & (-t2[this_dist]+t1[d1i] <= time_scale))[0].size
    # Add it to the running total.
    X = X + this
    # Now compute the time-proximate points for the sampling data.
    for i in range(nrand):
      this=0
      if t1leads:
        this = np.where((t2[this_dist] > randtimes[i][d1i]) &\
                        (t2[this_dist]-randtimes[i][d1i] <= time_scale))[0].size
      else:
        this = np.where((t2[this_dist] < randtimes[i][d1i]) &\
                        (-t2[this_dist]+randtimes[i][d1i] <= time_scale))[0].size
      randX[i] = randX[i] + this
  # Return the test statistic and the distribution.
  return X, randX
  

# Normalize the data a bit, and then compute the Knox test statistc.
# Also compute the distribution of the test with permuted time stamps
# to assess significance.
def knox(x1, y1, t1, x2, y2, t2, dist_scale, time_scale_days, nrand=1000, verbose=True):
  '''Compute the Knox test statistic:
     X = # events near in space and time versus time-permuted'''

  # First get rid of points where the spatial location is undefined.
  t1leads=True
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
    t1leads = False

  # Compute the test statistic for the real data and the randomized data.
  X, randX = compute_test_statistic(x1, y1, t1, Nd1, x2, y2, t2, Nd2, \
                                    dist_scale, time_scale, nrand=nrand, t1leads=t1leads, verbose=verbose)
  # OK, we're done now.
  return X, randX
