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
from multiprocessing.sharedctypes import RawArray
import myModule


def initProcess(share):
  myModule.c = share


def generateData(n, c):
    logging.info(f"Generating {n} samples in {c} classes")
    X, y = make_blobs(n_samples=n, centers = c, cluster_std=1.7, shuffle=False,
                      random_state = 2122)
    return X


def nearestCentroid(datum, centroids):
    # norm(a-b) is Euclidean distance, matrix - vector computes difference
    # for all rows of matrix
    dist = np.linalg.norm(centroids - datum, axis=1)
    return np.argmin(dist), np.min(dist)


def argumentListMaker(N,workers,data,centroids):
    intervalsize = int(N / workers)
    res = []
    current = 0
    while True:
        tup = (current,current+intervalsize,len(centroids),data,centroids)
        current += intervalsize
        res.append(tup)
        if current + intervalsize > N:
            res[-1] = (res[-1][0],N,len(centroids),data,centroids)
            break
    return res

def assignment(start,fin,k,data,centroids):
    variation = np.zeros(k)
    cluster_sizes = np.zeros(k, dtype=int)
    for i in range(start,fin):
        cluster, dist = nearestCentroid(data[i],centroids)
        myModule.c[i] = cluster
        cluster_sizes[cluster] += 1
        variation[cluster] += dist**2
    return cluster_sizes, variation

def kmeans(k, data, nr_iter = 100, workers = 1):
    N = len(data)

    # Choose k random data points as centroids
    centroids = data[np.random.choice(np.array(range(N)),size=k,replace=False)]
    logging.debug("Initial centroids\n", centroids)

    N = len(data)
    #print(N)
    #cc = RawArray(ctypes.c_int,N)
    #c = np.frombuffer(cc,dtype=int)    
    c = multiprocessing.Array('i',N)
    pool = multiprocessing.Pool(initializer=initProcess,initargs=(c,),processes=workers)


    # The cluster index: c[i] = j indicates that i-th datum is in j-th cluster
    #c = np.zeros(N, dtype=int)
    timing = [0,0]
    logging.info("Iteration\tVariation\tDelta Variation")
    total_variation = 0.0

    argumentlist = argumentListMaker(N,workers,data,centroids)
    for j in range(nr_iter):
        logging.debug("=== Iteration %d ===" % (j+1))

        start = time.time()
        # Assign data points to nearest centroid
        #print(c[:])
        s = pool.starmap(assignment,argumentlist)
        #print(c[:])
        
        timing[0] += time.time() - start
        total_variation = np.zeros(k,dtype=float)
        cluster_sizes = np.zeros(k,dtype=int)
        for i in range(len(s)):
            for j in range(len(cluster_sizes)):
                cluster_sizes[j] += s[i][0][j]
                #print(s[i][0][j])
            for j in range(len(total_variation)):
                total_variation[j] += s[i][1][j]
                #print(s[i][1][j])
        delta_variation = -total_variation
 #       total_variation = sum(variation) 
        delta_variation += total_variation
        #logging.info("%3d\t\t%f\t%f" % (j, total_variation, delta_variation))
        #print(delta_variation, total_variation)

        start = time.time()
        # Recompute centroids
        centroids = np.zeros((k,2)) # This fixes the dimension to 2
        for i in range(N):
            centroids[c[i]] += data[i]        
        timing[1] += time.time() - start
        centroids = centroids / cluster_sizes.reshape(-1,1)
        logging.debug(cluster_sizes)
        logging.debug(c)
        logging.debug(centroids)
  
    return total_variation, c, timing


def computeClustering(args):
    if args.verbose:
        logging.basicConfig(format='# %(message)s',level=logging.INFO)
    if args.debug: 
        logging.basicConfig(format='# %(message)s',level=logging.DEBUG)

    
    X = generateData(args.samples, args.classes)

    start_time = time.time()
    #
    # Modify kmeans code to use args.worker parallel threads
    total_variation, assignment, timing = kmeans(args.k_clusters, X, nr_iter = args.iterations,workers=args.workers)
    #
    #
    end_time = time.time()
    logging.info("Clustering complete in %3.2f [s]" % (end_time - start_time))
    print(f"Total variation {total_variation}")
    print("Overall time assignment: " + str(timing[0]) + " Avg time: " + str(timing[0]/args.iterations))
    print("Overall time centroids: " + str(timing[1])+ " Avg time: " + str(timing[1]/args.iterations))

    if args.plot: # Assuming 2D data
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.scatter(X[:, 0], X[:, 1], c=assignment, alpha=0.2)
        plt.title("k-means result")
        #plt.show()        
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

