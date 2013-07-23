#!/usr/bin/env python
# Implement the Knox test for spatio-temporal correlation

import numpy as np
import time, copy
from spatial_temporal_test import Spatial_Temporal_Test

class Knox(Spatial_Temporal_Test):
  
  def compute_test_statistic(self, x1, y1, t1, x2, y2, t2, dist_scale, \
                             time_scale, verbose=True, nrand=1000):
    '''
    Compute the Knox test statistic:
       X = # events near in space and time versus time-permuted
    Compute the distributio of the Test with permuted time stamps
    '''
    
    #ONCE SPT.preprocess_and_normalize is a decorator remove this call
    s = super(Knox, self).preprocess_and_normalize(x1, y1, t1, x2, y2, t2,\
          dist_scale, time_scale_days)
    
    t1prime = copy.deepcopy(t1)
    randtimes = []
    for i in range(nrand):
      np.random.shuffle(t1prime)
      randtimes.append(copy.deepcopy(t1prime))
    
    X = 0
    randX = np.zeros(nrand)
    # Loop over all points in (x1,y1,t1)
    Nd1 = len(t1)
    for d1i in range(Nd1):
      # Print out a handy status message in case the number of points
      # is extremely large and you're bored.
      if verbose and (d1i % 1000 == 0): print(d1i, Nd1)
      # Compute the number of space-proximate points in (x2,y2)
      this_dist = np.where(((x2-x1[d1i])*(x2-x1[d1i]) + (y2-y1[d1i])*(y2-y1[d1i]) \
                            <= dist_scale*dist_scale))
      # Now compute the time-proximate points from t2 for real data.
      this = np.where((np.abs(t2[this_dist]-t1[d1i]) <= \
                       time_scale))[0].size
      # Add it to the running total.
      X = X + this
      # Now compute the time-proximate points for the sampling data.
      for i in range(nrand):
        this = np.where((np.abs(t2[this_dist]-randtimes[i][d1i]) <= \
                         time_scale))[0].size
        randX[i] = randX[i] + this
    # Return the test statistic and the distribution.
    return X, randX

