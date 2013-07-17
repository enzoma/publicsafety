#!/usr/bin/env python

import numpy as np
import time

def compute_test_statistic(x1, y1, t1, Nd1, x2, y2, t2, Nd2, \
                           dist_scale, time_scale, verbose=True):
  X = 0
  for d1i in range(Nd1):
    if verbose and (d1i % 1000 == 0): print(d1i, Nd1)
    this = np.where(((x2-x1[d1i])*(x2-x1[d1i]) + (y2-y1[d1i])*(y2-y1[d1i]) \
                     <= dist_scale) & (np.abs(t2-t1[d1i]) <= \
                     time_scale))[0].size
    X = X + this

  return X
  

def knox(x1, y1, t1, x2, y2, t2, dist_scale, time_scale_days, nrand=1000):
  '''Compute the Knox test statistic:
     X = # events near in space and time versus time-permuted'''

  wh1 = np.where(~np.isnan(x1))
  wh2 = np.where(~np.isnan(x2))
  x1, y1, t1 = x1[wh1], y1[wh1], t1[wh1]
  x2, y2, t2 = x2[wh2], y2[wh2], t2[wh2]
  t1 = np.array([time.mktime(time.struct_time(i)) for i in t1])
  t2 = np.array([time.mktime(time.struct_time(i)) for i in t2])
  time_scale = time_scale_days * 24 * 3600
  Nd1 = len(t1)
  Nd2 = len(t2)
  if Nd1 > Nd2:
    x3, y3, t3, Nd3 = x1, y1, t1, Nd1
    x1, y1, t1, Nd1 = x2, y2, t2, Nd2
    x2, y2, t2, Nd2 = x3, y3, t3, Nd3

  X = compute_test_statistic(x1, y1, t1, Nd1, x2, y2, t2, Nd2, \
                             dist_scale, time_scale)
  randdist = []
  for i in range(nrand):
    np.random.shuffle(t1)
    randdist.append(\
      compute_test_statistic(x1, y1, t1, Nd1, x2, y2, t2, Nd2, \
                             dist_scale, time_scale))
  return X, randdist
