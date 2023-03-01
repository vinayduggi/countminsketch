import random
import numpy as np
import sys
from math import log, e, ceil
from collections import defaultdict

# Big prime for the use in creating hash functions
BIG_PRIME = 10089886811898868001

class CountMinSketch(object):
    """
    CountMinSketch class implementation with epsilon, delta, k, n as params
    The params epsilon : float and delta : float control the accuracy and certainity of the CountMinSketch
    epsilon and delta must be between 0 and 1 exclusive of the bounds

    Raises Exception
    -------------------
    If either of epsilon and delta or k and n are not provided

    Example to run
    -------------------
    cms = CountMinSketch(epsilon = 0.0003, delta = 0.0001)
    cms = CountMinSketch(k = 10000, n = 10)
    """

    # Input can be either epsilon and delta or k (number of buckets) and n (number of instances)
    def __init__(self, epsilon = None, delta =  None, k = None, n = None):

        self.total = 0
        if delta is not None and epsilon is not None:
            self.k = int(ceil(e/epsilon))
            self.n = int(ceil(log(1./delta)))
        elif k is not None and n is not None:
            self.k = k
            self.n = n
        else:
            raise Exception("Either number of buckets (k) and number of independent instances (n) or epsilon and delta must be supplied.")

        # Generate a table (matrix) (k*n) to store the counts 
        self.table_counts = np.zeros((self.n, self.k), dtype='int32')

        #Generate a list of hash functions using auxilary functions depending upon number of instances (n)
        self.random_hash_functions = [self.__hash_data() for i in range(self.n)]
    

    def __hash_data(self):
        """
        Generates and returns a hash function from a family of pairwise-independent functions
        i.e., Universal hash family
        a, b are random numbers less than prime number generated randomly using BIG_PRIME 
        as a bound for range (0, BIG_PRIME-1)
        that being said these hash functions are non-cryptographic in nature
        """
        a, b = random_param_generator(), random_param_generator()
        return lambda x: (a * x + b) % BIG_PRIME % self.k

    
    def update_element(self, x, increment_val = 1):
        """
        Function updates the stream element by the hash key generated
        by the value specified in the increment.

        Parameters
        ----------------
        x : string (The element to update the value of in the CMsketch)
        increment_val: int (The amount to update the key by given value )

        Example to run
        -----------------
        cms.update_element('CountMinSketch', 1)
        """

        for i, random_hash in enumerate(self.random_hash_functions):
            col = random_hash(abs(hash(x)))
            self.table_counts[i, col] += increment_val
        

    def estimate_element_count(self, x):
        """
        Function to return the CMSketch estimate of count for the provided key as hash

        Parameters
        ----------------
        x: string (The query element to which estimate is needed.)

        Return value
        ----------------
        minVal: int (The min estimate of all the instances for given hash key on the CMSketch)

        Example to run
        -----------------
        cms.estimate_element_count('CountMinSketch')
        """
        minVal = sys.maxsize
        for i, random_hash in enumerate(self.random_hash_functions):
            col = random_hash(abs(hash(x)))
            minVal = min(self.table_counts[i, col], minVal)
        
        return col, minVal



def random_param_generator():
    #Random integer generator for a, b << BIG_PRIME
    return random.randrange(0, BIG_PRIME-1)