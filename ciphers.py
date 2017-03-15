#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ciphers.py
#  
#  Copyright 2017 Jesse Rominske
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Program to quickly encipher a plaintext

import math
import sys
import factorize

# converts the letter input to numbers (using ASCII)
def textConvert(text):
	nums = []
	for t in list(text):
		nums.append(ord(t) - 65) #A should be 0, for example	
	return nums

# converts simple numbers into 4-long blocks
def numToBlock(nums):
	blocks = []
	prev = 26 # set to an invalid value to be an indicator
	for n in nums:
		if prev == 26: # this is invalid, so we know this means it can be replaced
			prev = n # store the number for next time
		else:
			blocks.append(n + (100 * prev)) # make 4-digit block from numbers
			prev = 26 #reset the value of prev to 26 for next time 		
	return blocks
	
# converts 4-long blocks into simple numbers
def blockToNum(blocks):
	nums = []
	for b in blocks:
		nums.append((b - (b % 100)) / 100) # append its first two digits
		nums.append(b % 100) # append its last two digits
	return nums

# converts number input to letters (using ASCII)
def numConvert(nums):
	text = ""
	for n in nums:
		text += (str(chr(n + 65)))
	return text
	
# finds an inverse of a given mod m
def modInverse(a, m):
	i = 1
	for i in range(1, m):
		if (a * i) % m == 1:
			print("Found inverse of " + str(a) + " mod " + str(m) + ": " + str(i))
			return i
	# the lines below will only execute if the loop finished and never returned i
	print("No inverse of " + str(a) + " mod " + str(m))
	return 1

# uses given affine cipher to encode a message
def affineEncode(plainText, a, b):
	plainNums = textConvert(plainText)
	cipherNums = []
	for p in plainNums:
		cipherNums.append(((p * a) + b) % 26)
	return numConvert(cipherNums)

# uses given affine cipher to decode a message
def affineDecode(cipherText, a, b):
	cipherNums = textConvert(cipherText)
	plainNums = []
	aBar = modInverse(a, 26)
	for c in cipherNums:
		plainNums.append(((c - b) * aBar) % 26)
	return numConvert(plainNums)
	
# uses given Vigenère cipher to decode a message
def vigenDecode(cipherText, key):
	cipherNums = textConvert(cipherText)
	keyNums = textConvert(key)
	plainNums = []
	i = 0
	for c in cipherNums:
		plainNums.append((c - keyNums[i % len(keyNums)]) % 26)
		i += 1
	return numConvert(plainNums)
	
# uses given modular exponentation cipher to encode message
def modExpEncode(plainText, p, e):
	plainBlocks = numToBlock(textConvert(plainText))
	cipherBlocks = []
	for b in plainBlocks:
		c = 1
		for i in range(0, e): # up to but not including the power
			c = (c * b) % p
		cipherBlocks.append(c)
	return cipherBlocks

# uses given modular exponentation cipher to decode message
def modExpDecode(cipherBlocks, p, e):
	d = modInverse(e, p-1)
	plainBlocks = []
	for c in cipherBlocks:
		pb = 1
		for i in range(0, d): # up to but not including the power
			pb = (pb * c) % p
		plainBlocks.append(pb)
	return numConvert(blockToNum(plainBlocks))
	
# uses given RSA cipher to decode message
def rsaDecode(cipherBlocks, e, n):
	factors = factorize.factorize(n) # will be a 2-tuple for RSA
	phi = (factors[0] - 1) * (factors[1] - 1)
	d = modInverse(e, phi)
	plainBlocks = []
	for c in cipherBlocks:
		pb = 1
		for i in range(0, d): # up to but not including the power
			pb = (pb * c) % n
		plainBlocks.append(pb)
	return numConvert(blockToNum(plainBlocks))

# main program structure
def main(args):
	#problems from Rosen, Elementary Number Theory, 5th ed.
	#8.1: 4
	print(affineEncode("THERIGHTCHOICE", 15, 14))
	#8.1: 6
	print(affineDecode("RTOLKTOIK", 3, 24))
	#8.2: 2
	print(vigenDecode("WBRCSLAZGJMGKMFV", "SECRET"))
	#8.3: 2
	print(modExpEncode("SWEETDREAMS", 2621, 7))
	#8.3: 4
	print(modExpDecode([1213, 902, 539, 1208, 1234, 1103, 1374], 2591, 13))
	#8.4: 8
	print(rsaDecode([504, 1874, 347, 515, 2088, 2356, 736, 468], 5, 2881))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
