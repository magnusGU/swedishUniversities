#!/usr/bin/env python
import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
import time
import matplotlib.pyplot as plt
from math import pi

def sample_pi(n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    #print("Hello from a worker")
    random.seed()
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s


def compute_pi(args):
    n = int(args.steps / args.workers)
    p = multiprocessing.Pool(args.workers)
    s = p.map(sample_pi, [n]*args.workers)

    n_total = n*args.workers
    s_total = sum(s)
    pi_est = (4.0*s_total)/n_total
    print(" Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, pi-pi_est))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute Pi using Monte Carlo simulation.',
        epilog = 'Example: mp-pi-montecarlo-pool.py -s 100000 -w 4'
    )
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes')
    parser.add_argument('--steps', '-s',
                        default='1000',
                        type = int,
                        help='Number of steps in the Monte Carlo simulation')
    args = parser.parse_args()
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
    print(results)
    print(speedup)
    plt.plot([1,2,4,8,16,32],[1,2,4,8,16,32], 'bo')
    plt.plot([1,2,4,8,16,32],speedup,'ro')
    plt.savefig("piplot.png")
