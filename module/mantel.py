#!/usr/bin/env python
# Implement the Mantel test for spatio-temporal correlation

import numpy as np
import copy
from spatial_temporal_test import Spatial_Temporal_Test

class Mantel(Spatial_Temporal_Test):


  def __init__(self, x1, y1, t1, x2, y2, t2):
    super(Mantel, self).__init__(x1, y1, t1, x2, y2, t2)

  def space_transformation(self, dist):
    return 20.0/(dist+1.0)

  def time_transformation(self, dist):
    return 700.0/(dist+1.0)

  def compute_transformed_space_distance(self,  x1, y1, t2_indices=None):
    t2_indices = range(len(self.t2)) if t2_indices == None else t2_indices
    return self.space_transformation(abs(x1-self.x2) + abs(y1-self.y2))

  def compute_transformed_time_distance(self, t1, t2_indices=None):
    t2_indices = range(len(self.t2)) if t2_indices == None else t2_indices
    return self.time_transformation(abs(t1-self.t2))

  @Spatial_Temporal_Test.preprocess_and_normalize_decorator
  def compute_test_statistic(self, t1_as_leading_indicator=False, dist_scale_feet=None, time_scale_days=None, verbose=True, nrand=1000):
    '''
    Compute the Mantel test statistic:
       X = # events near in space and time versus time-permuted
    Compute the distributio of the Test with permuted time stamps
    '''
    t1prime = copy.deepcopy(self.t1)
    #TODO: We are essentallcreating a nrand X len(t1prime) matrix
    #      So we should first do a check and see if the t1 is too
    #      large or (potentially nrand) to make this matrix. Otherwise
    #      we will have to do this on the fly
    randtimes = []
    for i in range(nrand):
      np.random.shuffle(t1prime)
      randtimes.append(copy.deepcopy(t1prime))
   
    randX = np.zeros(nrand)
    X = 0.0
    for d1i in range(self.N1):
      # Print out a handy status message in case the number of points
      # is extremely large and you're bored.
      if verbose and (d1i % 10 == 0): print(d1i, self.N1)

      close_in_time = self.get_time_proximate_points(self.t1[d1i], t1_as_leading_indicator)

      distances_space = self.compute_transformed_space_distance(self.x1[d1i], self.y2[d1i], close_in_time) 
      distances_time = self.compute_transformed_time_distance(self.t1[d1i], close_in_time)
      X  = X + sum(distances_space * distances_time)

      for i in range(nrand):
        rand_distances_time = self.compute_transformed_time_distance(randtimes[i][d1i], close_in_time)
        randX[i] = randX[i] + sum(distances_space * rand_distances_time) 

    # Return the test statistic (and the null distribution if the user wanted)
    if nrand > 0:
      return X, randX
    else:
      return X
