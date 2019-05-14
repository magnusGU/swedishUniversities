#!/usr/bin/env python
import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
import time
import multiprocessing
import matplotlib.pyplot as plt
from math import pi

def sample_pi(t):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    #print("Hello from a worker")
    q = t[0]
    n = t[1]
    i = t[2]
    random.seed(31415)
    while True:
        s = 0
        for i in range(n):
            x = random.random()
            y = random.random()
            if x**2 + y**2 <= 1.0:
                s += 1
        q.put(s)

def compute_pi(args):
    n = 100000
    p = multiprocessing.Pool(args.workers)
    q = multiprocessing.Manager().Queue()
    start = time.time()
    p.map_async(sample_pi, [(q,n,(i+3)**3) for i in range(args.workers)]*args.workers)
    s_total = 0
    n_total = 0
    pi_est = 0
    while abs(pi_est-pi) > args.accuracy:
        s_total += q.get()
        n_total += n
        pi_est = (s_total*4)/n_total
        if args.verbose:
            print("######### STATUS ##########")
            print("s_total: ", s_total)
            print("n_total: ",n_total)
            print("pi_est: ", pi_est)
            print("error: ", abs(pi_est-pi))
    end = time.time()
    print(" Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.7f\t%1.7f" % (n_total, s_total, pi_est, pi-pi_est))
    print("Total time: ",end-start)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute Pi using Monte Carlo simulation.',
        epilog = 'Example: mp-pi-montecarlo-pool.py -s 100000 -w 4'
    )
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes')
    parser.add_argument('--accuracy','-a',
                        default='0.01',
                        type=float,
                        help='Stop when this accuracy is reached')
    parser.add_argument('--verbose','-v',
                        action='store_true')
    args = parser.parse_args()
    #compute_pi(args)
    results = []
    for i in range(6):
        args.workers = 2**i
        start = time.time()
        compute_pi(args)
        end = time.time()
        results.append(end-start)
    speedup = [1.0]
    for i in range(1,len(results)):
        speedup.append(results[0]/results[i])
    plt.plot([1,2,4,8,16,32],[1,2,4,8,16,32], label="Theoretical speedup")
    plt.plot([1,2,4,8,16,32],speedup,label="Measured speedup")
    #plt.show()
    plt.legend(loc="best")
    plt.savefig("piplotb.png")
