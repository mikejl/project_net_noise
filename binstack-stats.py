#
# binstack-stats.py
# Mike Libassi
# 6/2/17
#
# pass in file with raw bits (0,1's) no spaces
# out: some stats
#
# #################################################

from __future__ import division
import math
import sys
import os
import scipy.special as spc
import numpy


count = 0
zeros = 0
ones = 0
pct_zero = 0.
pct_ones = 0.
#sample_size=100

infile = sys.argv[1]

with open(infile) as f:
    bin_data = f.read()

for char in bin_data:
    if char == '0':
        count = count - 1
        zeros = zeros + 1
    else:
        count = count + 1
        ones = ones + 1

stacktotal = len(bin_data)    
sobs = count / math.sqrt(stacktotal)
pct_zero =  (zeros / stacktotal) * 100 
pct_ones = (ones / stacktotal) * 100
Out_pct_zeros = format(pct_zero, '.3f')
Out_pct_ones = format(pct_ones, '.3f') 

print "Binay Stack size: ", stacktotal
print "Sobs: ", sobs
print "Count value (-1 if 0 and +1 if 1): ", count
print "Zero total: ", zeros, " Ones total: ", ones
print "% ones: ", Out_pct_ones, " % zeros: ", Out_pct_zeros




