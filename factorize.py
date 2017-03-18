#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  factorize.py
#  
#  Copyright 2017 Jesse Rominske
#  
#  Functions to print the prime power factorization of n

import math

# returns primality of i
def isPrime(i, primes):
	if i == 2: return True
	for p in primes:
		if p <= math.sqrt(i):
			if i % p == 0: return False
		else: return True

# return the prime factors of n (as a list of integers)
def factorize(n):
	primes = [] # list of primes we will use to compare primality
	factors = [] # list of factors we have found so far
	bound = int(math.ceil(math.sqrt(n) + 1)) # bound to limit looping
	i = 2 # the number we will be checking for primality and division
	while i < bound:
		if isPrime(i, primes):
			primes.append(i)
			divides = False
			while n % i == 0:
				divides = True
				factors.append(i)
				n /= i
			if divides: bound = int(math.ceil(math.sqrt(n) + 1))
		i += 1
	if n > 1: factors.append(n) # this must be larger than all p, so the list is still sorted
	return factors
