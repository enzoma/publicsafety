#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

class Spatial_Temporal_Test:
  __metaclass__ = ABCMeta
  
  #TURN THIS INTO A DECORATOR
  def preprocess_and_normalize(self, x1, y1, t1, x2, y2, t2, dist_scale, time_scale_days):
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
  
  # Normalize the data a bit, and then compute the Knox test statistc.
  # Also compute the distribution of the test with permuted time stamps
  # to assess significance.

  #HAVE PREPROCESS AND NORMALIZE DECORATE THIS METHOD
  @abstractmethod
  def compute_test_statistic(self, x1, y1, t1, x2, y2, t2, dist_scale, time_scale_days, verbose=True, nrand=1000):
    pass
  
