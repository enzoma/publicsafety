#!/usr/bin/env python
# Implement the Knox test for spatio-temporal correlation

import numpy as np
import copy
from spatial_temporal_test import Spatial_Temporal_Test

class Knox(Spatial_Temporal_Test):


  def __init__(self, x1, y1, t1, x2, y2, t2):
    super(Knox, self).__init__(x1, y1, t1, x2, y2, t2)
  
  #TODO: Need to create a new deocroator that will take X and potentially randX, and return p_value
  @Spatial_Temporal_Test.preprocess_and_normalize_decorator
  def compute_test_statistic(self, dist_scale_feet, time_scale_days, t1_as_leading_indicator=False, verbose=True, nrand=1000): 
    '''
    Compute the Knox test statistic:
       X = # events near in space and time versus time-permuted
    Compute the distributio of the Test with permuted time stamps

    dist_scale_feet = how many feet designates close in space
    time_scale_days = how many days designates clase in time
    t1_as_leading_indicator = if you one to do a one-sided test--i.e. when process_1 procedes pocess_2 in time (but still within time_scale_days) 
    '''
    
    t1prime = copy.deepcopy(self.t1)
    #TODO: We are essentally creating a nrand X len(t1prime) matrix
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
      if verbose and (d1i % 10 == 0): print(d1i, self.N1)
      # Compute the number of space-proximate points in (x2,y2)
      close_in_space = np.where(((self.x2-self.x1[d1i])**2 + (self.y2-self.y1[d1i])**2 \
                            <= dist_scale_feet**2))[0]
      print len(close_in_space)
      # Now compute the time-proximate points from t2 for real data.
      #TODO: Need to determine if they asked for a one-sided vs two sided test (and if had to switch t1 and t2)
      close_in_space_time = self.get_time_proximate_points(time_scale_days, self.t1[d1i], close_in_space, t1_as_leading_indicator)
   
      # Add it to the running total.
      X = X + len(close_in_space_time)
       
      # Now compute the time-proximate points for the sampling data.
      #TODO: Need to determine if they asked for a one-sided vs two sided test (and if had to switch t1 and t2)
      for i in range(nrand):
        close_in_space_time = self.get_time_proximate_points(time_scale_days, randtimes[i][d1i], close_in_space, t1_as_leading_indicator)
        randX[i] = randX[i] + len(close_in_space_time)
   
    # Return the test statistic (and the null distribution if the user wanted)
    if nrand > 0:
      return X, randX
    else:
      return X

