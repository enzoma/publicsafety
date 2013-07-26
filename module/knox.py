#!/usr/bin/env python
# Implement the Knox test for spatio-temporal correlation

import numpy as np
import copy
from spatial_temporal_test import Spatial_Temporal_Test

class Knox(Spatial_Temporal_Test):


  def __init__(self, x1, y1, t1, x2, y2, t2):
    super(Knox, self).__init__(x1, y1, t1, x2, y2, t2)

  @Spatial_Temporal_Test.preprocess_and_normalize_decorator
  def compute_test_statistic(self, dist_scale, time_scale, verbose=True, nrand=1000):
    '''
    Compute the Knox test statistic:
       X = # events near in space and time versus time-permuted
    Compute the distributio of the Test with permuted time stamps
    '''
    
    #ONCE SPT.preprocess_and_normalize is a decorator remove this call
    #  s = super(Knox, self).preprocess_and_normalize(x1, y1, t1, x2, y2, t2,\
    #          dist_scale, time_scale_days)
   
    t1prime = copy.deepcopy(self.t1)
    #TODO: We are essentallcreating a nrand X len(t1prime) matrix
    #      So we should first do a check and see if the t1 is too
    #      large or (potentially nrand) to make this matrix. Otherwise
    #      we will have to do this on the fly
    randtimes = []
    for i in range(nrand):
      np.random.shuffle(t1prime)
      randtimes.append(copy.deepcopy(t1prime))
    
    X = 0
    randX = np.zeros(nrand)
    # Loop over all points in (x1,y1,t1)
    for d1i in range(self.N1):
      # Print out a handy status message in case the number of points
      # is extremely large and you're bored.
      if verbose and (d1i % 1000 == 0): print(d1i, self.N1)
      # Compute the number of space-proximate points in (x2,y2)
      this_dist = np.where(((self.x2-self.x1[d1i])**2 + (self.y2-self.y1[d1i])**2 \
                            <= dist_scale**2))
      # Now compute the time-proximate points from t2 for real data.
      this = np.where((np.abs(self.t2[this_dist]-self.t1[d1i]) <= \
                       time_scale))[0].size

      # Add it to the running total.
      X = X + this
       
      # Now compute the time-proximate points for the sampling data.
      for i in range(nrand):
        this = np.where((np.abs(self.t2[this_dist]-randtimes[i][d1i]) <= \
                         time_scale))[0].size
        randX[i] = randX[i] + this
    
    # Return the test statistic (and the null distribution if the user wanted)
    if nrand > 0:
      return X, randX
    else:
      return X

