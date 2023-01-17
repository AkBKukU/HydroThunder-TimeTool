#!/usr/bin/python3

# This script is used to confirm the checksum variables found work as expected without the complexity of the other scripts (math not fully verified)

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

checksum_offset_skip = 0x17
data_start_offset = 0x75BE660 + checksum_offset_skip

checksum_seed = 0xFEDCBA94 # Result of of -0x0123456b

# ==============================================================================

print()

print("Checking cmos area has correct offset in .img files")
verifyImageHeaders([cmos_image_path], cmos_img_offset)

print()

print("Checksum from image : {}".format(getChecksum('SUM32', cmos_image_path, 0x75BE66F).hex(' ')))

print()

algorithm_list = ['SUM8', 'SUM16', 'SUM32']
checksum_lengths = [cmos_area_length, cmos_area_length, cmos_area_length]

for i in range(len(algorithm_list)):
	checksum, checksum_start_offset, checksum_end_offset, num_sums, last_byte = calculateChecksum(algorithm_list[i], 'little', cmos_image_path, 0x75BE677, checksum_lengths[i], checksum_seed)
	print("{:5s}  {:12s}  {:10s} → {:10s}  {:5d}".format(algorithm_list[i], checksum.hex(' '), checksum_start_offset.to_bytes(4,'big').hex(), checksum_end_offset.to_bytes(4,'big').hex(), num_sums))


print()

# Output from checksum must match "Checksum from image" output
