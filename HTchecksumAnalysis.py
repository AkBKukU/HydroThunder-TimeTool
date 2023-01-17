#!/usr/bin/python3

# This script just looks at the checksums and data checksums to see if there's anything statistically obvious about them

import sys
import os
import struct
import datetime
import math
import glob

from HTchecksumUtils import *

cmos_image_paths = glob.glob('./DataSamples/*.img')

cmos_start_offsets = [  0x75BE663,		# Offset for CF card first occurrence
						0x75EE663		# Offset for CF card second occurrence
					 ]

checksum_offset_skip = 0x17

cmos_area_offsets = [  0x75BE660 + checksum_offset_skip,		# Only checksum data after the checksum which might be different. Don't include the "checksum itself in our checksum"
						0x75EE660 + checksum_offset_skip		# 
					 ]

#cmos_area_length = 0x147A		# Measured length of one of the duplicated cmos data section
cmos_area_length = 0x1500		# Measured length plus some padding


checksum_offsets = [0x75BE66F, 			# Checksum suspected to be for operator settings, changed with track/ai diff, observed overflow into this byte, likely 2 byte or 4 byte
					0x75EE66F
					]

checksum_endian = 'little'
checksum_seed = 0x00000000
checksum_seed = 0xFEDCBA94 # Result of of -0x0123456b

# ==============================================================================

print()

print("Checking cmos area has correct offset in .img files [First Occurrence]")
verifyImageHeaders(cmos_image_paths, cmos_start_offsets[0])
print("Checking cmos area has correct offset in .img files [Second Occurrence]")
verifyImageHeaders(cmos_image_paths, cmos_start_offsets[1])

print("\n                                 |  Midway's   | My checksum")
print("                                 |  Checksum   | Calculated with SUM32")

first_checksums = []
second_checksums = []
diff_checksums = []
diff_cmos_checksums = []
diff_midway_my_checksums = []

cmos_image_consistent = []
cmos_image_paths_consistent = []

for cmos_image_idx in range(len(cmos_image_paths)):
	print("\n\n {:3d} [{}]".format(cmos_image_idx, cmos_image_paths[cmos_image_idx]))

	first_checksums.append(getChecksum('SUM32', cmos_image_paths[cmos_image_idx], checksum_offsets[0]))
	second_checksums.append(getChecksum('SUM32', cmos_image_paths[cmos_image_idx], checksum_offsets[1]))
		
	first_checksum_int = int.from_bytes(first_checksums[cmos_image_idx], checksum_endian, signed=False)
	second_checksum_int = int.from_bytes(second_checksums[cmos_image_idx], checksum_endian, signed=False)
	diff_checksum_int = second_checksum_int - first_checksum_int
	diff_checksums.append(abs(diff_checksum_int).to_bytes(4, checksum_endian, signed=False))
	
	first_cmos_checksum,_,_,_,_ = calculateChecksum('SUM32', checksum_endian, cmos_image_paths[cmos_image_idx], cmos_area_offsets[0], cmos_area_length, checksum_seed)
	second_cmos_checksum,_,_,_,_ = calculateChecksum('SUM32', checksum_endian, cmos_image_paths[cmos_image_idx], cmos_area_offsets[1], cmos_area_length, checksum_seed)
	
	first_cmos_checksum_int = int.from_bytes(first_cmos_checksum, checksum_endian, signed=False)
	second_cmos_checksum_int = int.from_bytes(second_cmos_checksum, checksum_endian, signed=False)
	diff_cmos_checksum_int = second_cmos_checksum_int - first_cmos_checksum_int
	diff_cmos_checksums.append(abs(diff_cmos_checksum_int).to_bytes(4, checksum_endian, signed=False))
	
	midway_my_checksum_int = first_checksum_int - first_cmos_checksum_int
	diff_midway_my_checksums.append(abs(midway_my_checksum_int).to_bytes(4, checksum_endian, signed=False))
	
	first_checksum_bin = "{:032b}".format(first_checksum_int)
	second_checksum_bin = "{:032b}".format(second_checksum_int)
	diff_checksum_bin = "{:032b}".format(abs(diff_checksum_int))
	
	print("Checksum for first cmos copy     : {} | {} {}".format(first_checksums[cmos_image_idx].hex(' '), first_cmos_checksum.hex(' '), first_checksum_bin))
	print("Checksum for second cmos copy    : {} | {} {}".format(second_checksums[cmos_image_idx].hex(' '), second_cmos_checksum.hex(' '), second_checksum_bin))
	print("Checksum abs diff between copies : {} | {} {}".format(diff_checksums[cmos_image_idx].hex(' '), diff_cmos_checksums[cmos_image_idx].hex(' '), diff_checksum_bin), end='')
	
	if diff_checksum_int > 0:
		print(" HIGHER CHECKSUM  <--")
		cmos_image_consistent.append(False)
	elif diff_checksum_int < 0:
		print(" LOWER CHECKSUM   <--")
		cmos_image_consistent.append(False)
	else:
		print(" NO DIFF, CMOS AREAS IDENTICAL")
		cmos_image_consistent.append(True)
		cmos_image_paths_consistent.append(cmos_image_paths[cmos_image_idx])
		
	print("Checksum abs diff between midway :               {}".format(diff_midway_my_checksums[cmos_image_idx].hex(' '), end=''), end='')
	
	if midway_my_checksum_int == 0:
		print(" Valid Checksum!", end='')
	
print("\n                                 |  Midway's   | My checksum")
print("                                 |  Checksum   | {} {} {}".format('SUM32', checksum_endian, checksum_seed))


# List of image files with all the ones with inconsistent "checksums" removed
# Print this list and copy paste it into HTchecksumButeForceFind
#print(cmos_image_paths_consistent)


# Note the upper 2 MSBs in the "Checksum" are sometimes different between the two "checksums" of the two data blocks
