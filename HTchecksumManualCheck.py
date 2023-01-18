#!/usr/bin/python3

# Use this script to quickly compare checksums stored in an image and the SUM32 checksum of the actual data, useful for calculating a new checksum after changing the data
# 
# Call with `HTchecksumManualCheck.py` or `HTchecksumManualCheck.py './DataSamples/Pay.img'`

import sys
import os
import struct
import datetime
import math

from HTchecksumUtils import *

if len(sys.argv) > 1:
	image_path = sys.argv[1]
else:
	image_path = './DataSamples/SN33-Real.img'

cmos_base_offsets 		= [0x75BE663, 0x75EE663]	# Address of first byte of the CMOS 'header' [01 00 00 00 98 ba dc fe]
checksum_rel_offset 	= 0xC						# Relative bytes between 'cmos_base_offsets' and the first byte of the checksum
area_rel_offset			= 0x14						# Relative bytes between 'cmos_base_offsets' and the first byte of the area being checksumed
area_length 			= 0x1500					# Number of bytes included in the checksum (must be modulo of 4 due to SUM32 4 byte width)
checksum_seed 			= 0xFEDCBA94				# Checksum seed

# ==============================================================================

print("\nChecking supplied offsets point to start of CMOS areas in image:")
verifyImageHeaders([image_path], cmos_base_offsets[0])
verifyImageHeaders([image_path], cmos_base_offsets[1])

print()
print("                                  |     Old      |    Newly     |                       ")
print("                                  |    Stored    |  Calculated  |                       ")
print("                                  |   Checksum   |   Checksum   |  Checksum Area Span   ")
print("----------------------------------|--------------|--------------|-----------------------")

checksums_old = []
checksums_new = []

# For each CMOS block (there's two)
for this_cmos_copy in range(len(cmos_base_offsets)):

	# Read old checksum from image at current CMOS block
	checksum_abs_offset = cmos_base_offsets[this_cmos_copy] + checksum_rel_offset
	checksums_old.append(readChecksum(image_path, checksum_abs_offset))
	
	# Calculate new checksum from image at current CMOS block
	area_checksum_result, area_start_offset, area_end_offset, num_sums, last_byte = calculateChecksum(image_path, cmos_base_offsets[this_cmos_copy] + area_rel_offset)
	checksums_new.append(area_checksum_result)
		
	print("CMOS area #{:1d} Checksum @ {} | {:12s} | {:12s} | {} → {} ".format(this_cmos_copy, hex(checksum_abs_offset), checksums_old[this_cmos_copy].hex(' '), checksums_new[this_cmos_copy].hex(' '), hex(area_start_offset), hex(area_end_offset)))
	
print()
