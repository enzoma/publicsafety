#  CLUSTERING:
#   1) NORMALIZE THE FEATURES (ie, crime types) to each 
#   have mean 0 and sd = 1
#   2) Perform clustering again to determine optimal k 
#   3) Get cluster assignments from optimal k
#   4) Determine what each of these clusters corresponds to by
#   examining the relative representation of each crime type
#   in each cluster center
import csv
import numpy
import scipy
import matplotlib
import pylab
from sklearn.cluster import KMeans

# Create a 2d array of rows, converted strings to floats  
f = open("V2_normalized_crime_by_tract_per_thousand.csv", 'rb')
myreader = csv.reader(f)
header = myreader.next()
    # It might be necessary to remove certain characters if
    # an error message appears
    # in Vi: "ESC :" to get into document
    # %s to replace
    # / (cntrl-v) cntrl-m
    # / (cntrl-v) enter
    # /g
    # enter
x = list(myreader)
result = numpy.array(x).astype('float')

# Omit tract number from clustering
new_data = result[:,1:]

n_clusters = range(2,25)
  performance = []
  for k in n_clusters:
    clusterer = KMeans(init="k-means++", n_clusters = k, n_init = 10)
    clusterer.fit(new_data)
    preds = clusterer.predict(new_data)
    performance.append(clusterer.inertia_)

# How many clusters to use?
matplotlib.pyplot.grid(True)
matplotlib.pyplot.scatter(n_clusters, performance)
matplotlib.pyplot.show()

# Decided to use 7 clusters
 clusterer = KMeans(init="k-means++", n_clusters = 7, n_init = 10)
 clusterer.fit(new_data)
 clusterer.predict(new_data) #shows cluster assignment for each tract

a = clusterer.predict(new_data)
numpy.savetxt("V2_normalized_cluster_assignments.csv", a, delimiter=",")

# For each cluster, run the following to determine the relative
# representation of each crime type in each cluster
# tmp = clusterer.cluster_centers_[0]
# matplotlib.pyplot.grid(True)
# matplotlib.pyplot.scatter(range(len(tmp)), tmp)
# matplotlib.pyplot.show()

# Useful stuff:
# clusterer.cluster_centers_ # gives cluster centers in n-dimensional space for each cluster
