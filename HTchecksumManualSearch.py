#!/usr/bin/python3

# This script was just for me poking around seeing if I could find anything manually

import sys
import os
import struct
import datetime
import math

from HTchecksumUtils import *

cmos_image_path = './DataSamples/SN33-Real.img'

cmos_img_offset = 0x75BE663		# Default offset for CF card first occourance
#cmos_img_offset = 0x75EE663	# Default offset for CF card second occurrence

#cmos_area_length = 0x147A		# Measured length of one of the duplicated cmos data section
cmos_area_length = 0x1500		# Measured length plus some padding
#cmos_area_length = 0x0F		# DEBUG: Force small problem space

checksum_candidate_offset = [0x55BE66F 			# Checksum suspected to be for operator settings, changed with track/ai diff, observed overflow into this byte, likely 2 byte or 4 byte
							 ]
							 
suspected_checksum_offset = checksum_candidate_offset[0]

# ==============================================================================

print()
print("Checking cmos area has correct offset in .img files")

verifyImageHeaders([cmos_image_path], cmos_img_offset)

print()

print("Checksums from image : {}".format(getChecksum('SUM32', cmos_image_path, 0x75BE66F).hex(' ')))

print()

algorithm_list = ['SUM8', 'SUM16', 'SUM32']

print("\n=== Checksums for Operator data")

start = 0x75BE673
length = 0x164

op_sets_checksum = []
for i in range(len(algorithm_list)):
	checksum, checksum_start_offset, checksum_end_offset, num_sums, last_byte = calculateChecksum(algorithm_list[i], 'little' , cmos_image_path, start, length)
	print("{:5s}  {:12s}  {:10s} → {:10s}  {:5d}".format(algorithm_list[i], checksum.hex(' '), checksum_start_offset.to_bytes(4,'big').hex(), checksum_end_offset.to_bytes(4,'big').hex(), num_sums))
	op_sets_checksum.append(checksum)

print("\n=== Checksums for high score data")

start = 0x75BE7DF
length = 0x410

high_score_checksum = []
for i in range(len(algorithm_list)):
	checksum, checksum_start_offset, checksum_end_offset, num_sums, last_byte = calculateChecksum(algorithm_list[i], 'little' , cmos_image_path, start, length)
	print("{:5s}  {:12s}  {:10s} → {:10s}  {:5d}".format(algorithm_list[i], checksum.hex(' '), checksum_start_offset.to_bytes(4,'big').hex(), checksum_end_offset.to_bytes(4,'big').hex(), num_sums))
	high_score_checksum.append(checksum)


print("\n=== Checksums for hud split data")

start = 0x075bebf3
length = 0x104

time_split_checksum = []
for i in range(len(algorithm_list)):
	checksum, checksum_start_offset, checksum_end_offset, num_sums, last_byte = calculateChecksum(algorithm_list[i], 'little' , cmos_image_path, start, length)
	print("{:5s}  {:12s}  {:10s} → {:10s}  {:5d}".format(algorithm_list[i], checksum.hex(' '), checksum_start_offset.to_bytes(4,'big').hex(), checksum_end_offset.to_bytes(4,'big').hex(), num_sums))
	time_split_checksum.append(checksum)
	
	
print("\n\n")

algorithm_idx = 0

print(time_split_checksum[algorithm_idx])

a = high_score_checksum[algorithm_idx]
b = time_split_checksum[algorithm_idx]
c = op_sets_checksum[algorithm_idx]

a = int.from_bytes(a, 'little', signed=False)
b = int.from_bytes(b, 'little', signed=False)
c = int.from_bytes(c, 'little', signed=False)

checksum_sum = (a + b + c) % 0xFFFFFFFF
checksum_sum_bytes = checksum_sum.to_bytes(4,'little', signed=False)
			
			
print(checksum_sum_bytes.hex(' '))
