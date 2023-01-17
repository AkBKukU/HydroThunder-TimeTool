#!/usr/bin/python3

# This script verifies the HTchecksumUtils.py fuctions are working correctly

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

checksum_candidate_offset = [0x75BE66F 			# Checksum suspected to be for operator settings, changed with track/ai diff, observed overflow into this byte, likely 2 byte or 4 byte
							 ]
							 
suspected_checksum_offset = checksum_candidate_offset[0]

# ==============================================================================

print()

print("Checking cmos area has correct offset in .img files")
verifyImageHeaders([cmos_image_path], cmos_img_offset)

print()

print("Checksum from image : {}".format(getChecksum('SUM32', cmos_image_path, 0x75BE66F).hex(' ')))

print()

algorithm_list = ['SUM8', 'SUM16', 'SUM24', 'SUM32']
checksum_lengths = [1000, 1000, 999, 1000]

for i in range(len(algorithm_list)):
	checksum, checksum_start_offset, checksum_end_offset, num_sums, last_byte = calculateChecksum(algorithm_list[i], 'little', cmos_image_path, 0x075be85b, checksum_lengths[i])
	print("{:5s}  {:12s}  {:10s} → {:10s}  {:5d}".format(algorithm_list[i], checksum.hex(' '), checksum_start_offset.to_bytes(4,'big').hex(), checksum_end_offset.to_bytes(4,'big').hex(), num_sums))



print()


# Expected output

#Checking cmos area has correct offset in .img files
#  Image # 0 PASS : Found [01 00 00 00]   [./DataSamples/SN33-Real.img]
#
#Checksum from image : ea 75 09 e9
#
#SUM8   36            075be85b   → 075bec42     1000
#SUM16  59 dc         075be85b   → 075bec42      500
#SUM24  b8 a3 97      075be85b   → 075bec41      333
#SUM32  2d 20 2c bc   075be85b   → 075bec42      250
