#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
import copy, time
import numpy as np

class Spatial_Temporal_Test:
  __metaclass__ = ABCMeta

  def __init__(self, x1, y1, t1, x2, y2, t2):
    # Determine the array sizes. We're going to be looping over (x1,y1,t1),
    # so make sure that's the shorter of the two data sets to take maximal
    # advantage of numpy's parallelization for vectorized operations.
    self.N1 = len(t1)
    self.N2 = len(t2)
    if self.N1 < self.N2:
      self.x1, self.y1, self.t1 = x1, y1, t1
      self.x2, self.y2, self.t2 = x2, y2, t2
    else:
      self.x1, self.y1, self.t1 = x2, y2, t2
      self.x2, self.y2, self.t2 = x1, y1, t1

  @classmethod
  def preprocess_and_normalize_decorator(self, test_statistics_function):
    def toR(self, dist_scale, time_scale_days, verbose=True, nrand=1000):
      wh1 = np.where(~np.isnan(self.x1))
      wh2 = np.where(~np.isnan(self.x2))

      self.x1, self.y1, self.t1, self.N1 = self.x1[wh1], self.y1[wh1], self.t1[wh1], len(wh1[0])
      self.x2, self.y2, self.t2, self.N2 = self.x2[wh2], self.y2[wh2], self.t2[wh2], len(wh2[0])


      # Now compute the times in seconds for easy math. 
      self.t1 = np.array([time.mktime(time.struct_time(i)) for i in self.t1])
      self.t2 = np.array([time.mktime(time.struct_time(i)) for i in self.t2])
      time_scale = time_scale_days * 24 * 3600

      return test_statistics_function(self, dist_scale, time_scale, verbose, nrand)
   
    return toR

  #DECORATE THIS METHOD WITH THE  PROCESS_AND_NORMALIZE DECORATER
  @abstractmethod
  def compute_test_statistic(self, dist_scale, time_scale_days, verbose=True, nrand=1000):
    pass
