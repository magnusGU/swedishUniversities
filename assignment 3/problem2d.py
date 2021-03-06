#!/usr/bin/env python
#
# File: kmeans.py
# Author: Alexander Schliep (alexander@schlieplab.org)
#
#
import logging
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import time
import multiprocessing
import ctypes
import time

var_dict = {}

def initProcess(data,c):
    var_dict['data'] = data
    var_dict['c'] = c


def generateData(n, c):
    logging.info(f"Generating {n} samples in {c} classes")
    X, y = make_blobs(n_samples=n, centers = c, cluster_std=1.7, shuffle=False,
                      random_state = 212)
    return X


def nearestCentroid(datum, centroids):
    # norm(a-b) is Euclidean distance, matrix - vector computes difference
    # for all rows of matrix
    dist = np.linalg.norm(centroids - datum, axis=1)
    return np.argmin(dist), np.min(dist)

def assignment(start,fin,k,centroids):
    variation = np.zeros(k)
    for i in range(start,fin):
        cluster, dist = nearestCentroid(var_dict['data'][i],centroids)
        var_dict['c'][i] = cluster
        variation[cluster] += dist**2
    return variation

def computeCentroids(s,f,k):
    centroids = np.zeros((k,2))
    for i in range(s,f):
        centroids[var_dict['c'][i]] += var_dict['data'][i]   

    return centroids


def kmeans(k, data, nr_iter = 100, workers = 1):
    N = len(data)

    # Choose k random data points as centroids
    centroids = [data[0],data[44],data[4]]
    logging.debug("Initial centroids\n", centroids)

    N = len(data) 
    c = multiprocessing.Array('i',N)
    pool = multiprocessing.Pool(initializer=initProcess,initargs=(data,c,),processes=workers)


    # The cluster index: c[i] = j indicates that i-th datum is in j-th cluster
    timing = [0,0]
    logging.info("Iteration\tVariation\tDelta Variation")
    total_variation = 0.0

    for j in range(nr_iter):
        
        logging.debug("=== Iteration %d ===" % (j+1))

        start = time.time()
        # Assign data points to nearest centroid
        s = pool.starmap(assignment,[(i*(N//workers),(i+1)*(N//workers),k,centroids) for i in range(workers)])
        
        timing[0] += time.time() - start
        total_variation = np.zeros(k,dtype=float)
        cluster_sizes = np.zeros(k,dtype=int)
        for i in range(len(c)):
                cluster_sizes[c[i]] += 1

        start = time.time()
        # Recompute centroids
        centroids = np.zeros((k,2)) # This fixes the dimension to 2
     
        s = pool.starmap(computeCentroids,[(i*(N//workers),(i+1)*(N//workers),k) for i in range(workers)])
       

        for i in range(len(s)):
            centroids += s[i]
       
        timing[1] += time.time() - start
        
        centroids = centroids / cluster_sizes.reshape(-1,1)
        logging.debug(cluster_sizes)
        logging.debug(c[:])
        logging.debug(centroids)
  
    return total_variation, c, timing


def computeClustering(args):
    if args.verbose:
        logging.basicConfig(format='# %(message)s',level=logging.INFO)
    if args.debug: 
        logging.basicConfig(format='# %(message)s',level=logging.DEBUG)

    
    X = generateData(args.samples, args.classes)

    
    X = generateData(args.samples, args.classes)
    plt.plot([1,4,8,16,32],[1,4,8,16,32], 'bo')
    start_time = time.time()
    total_variation, assignment, timing = kmeans(args.k_clusters, X, args.iterations, 1)
    end_time = time.time()
    if args.verbose:
        print("Nr of cores: 1")
        print("Timing: " + str(timing))
        print("Time: " + str(end_time - start_time))
    ogTime = (end_time - start_time)
    plt.plot(1,1, 'ro')
    for i in [4,8,16,32]:
        start_time = time.time()
        total_variation, assignment, timing = kmeans(args.k_clusters, X, args.iterations, i)
        end_time = time.time()
        if args.verbose:
            print("Nr of cores: ",i)
            print("Timing: " + str(timing))
            print("Time: " + str(end_time - start_time))
        speedUp = ogTime / (end_time - start_time)
        plt.plot(i,speedUp, 'ro')
    plt.axis([0, 33, 0, 33])
    plt.show()
    plt.savefig("nplot.png")
    logging.info("Clustering complete in %3.2f [s]" % (end_time - start_time))
    print(f"Total variation {total_variation}")
    print("Overall time assignment: " + str(timing[0]) + " Avg time: " + str(timing[0]/args.iterations))
    print("Overall time centroids: " + str(timing[1])+ " Avg time: " + str(timing[1]/args.iterations))

    if args.plot: # Assuming 2D data
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.scatter(X[:, 0], X[:, 1], c=assignment, alpha=0.2)
        plt.title("k-means result")
        fig.savefig(args.plot)
        plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute a k-means clustering.',
        epilog = 'Example: kmeans.py -v -k 4 --samples 10000 --classes 4 --plot result.png'
    )
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes to use (NOT IMPLEMENTED)')
    parser.add_argument('--k_clusters', '-k',
                        default='3',
                        type = int,
                        help='Number of clusters')
    parser.add_argument('--iterations', '-i',
                        default='10',
                        type = int,
                        help='Number of iterations in k-means')
    parser.add_argument('--samples', '-s',
                        default='1000',
                        type = int,
                        help='Number of samples to generate as input')
    parser.add_argument('--classes', '-c',
                        default='3',
                        type = int,
                        help='Number of classes to generate samples from')   
    parser.add_argument('--plot', '-p',
                        type = str,
                        help='Filename to plot the final result')   
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Print verbose diagnostic output')
    parser.add_argument('--debug', '-d',
                        action='store_true',
                        help='Print debugging output')
    args = parser.parse_args()
    computeClustering(args)

