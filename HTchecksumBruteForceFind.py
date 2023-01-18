#!/usr/bin/python3

# This script attempts to brute force the start and end offsets for suspected checksums in the Hydro Thunder CMOS data. Currently only very basic SUM8, SUM16, SUM24 and SUM32 are implemented and tested. 
# This script first recursively searches the CMOS area for continuous blocks of data that checksum to the same value as the suspected checksum bytes, 
# once a match is found it then checksums the same block of data in another CMOS image and checks if the suspected checksum bytes of that image match the checksum of the block of data, 
# if the checksum reflects the block in all images, then the script pauses. 
# Note: when searching data areas containing the checksum itself, the script will find a valid block at the checksum offset with a span of 1

import sys
import os
import time

from HTchecksumUtils import *

# Use only images of the CMOS data with valid and matching checksums and data, ensure checksums and data between the two duplicates of the CMOS area is equal in HTchecksumsAnalysis.py
cmos_image_paths = ['./DataSamples/CF-Data-Set-datetime.img', 
'./DataSamples/CF-Data-Set-Free1st.img', 
'./DataSamples/CF-Data-Set-Vol-AttractEn.img', 
'./DataSamples/CF-Data-Set-SelTime-Track.img', 
'./DataSamples/CF-Data-Set-AllBoats.img', 
'./DataSamples/CF-Data-Set-Vol-Master.img', 
'./DataSamples/CF-Data-Set-FreeMulti.img', 
'./DataSamples/CF-Data-Set-Metric.img', 
'./DataSamples/CF-Data-Trackdiff.img', 
'./DataSamples/CF-Data-Set-AllTracks.img', 
'./DataSamples/CF-Data-Set-FreeLimit.img', 
'./DataSamples/Pay.img', 
'./DataSamples/CF-Data-NetID.img', 
'./DataSamples/CF-Data-AIDiff.img', 
'./DataSamples/CF-Data-Set-TrackOne.img', 
'./DataSamples/CF-Data-Set-SelTime-HIGH.img', 
'./DataSamples/CF-Data-Set-P-Standard.img', 
'./DataSamples/CF-Data-AIDiff-Big.img', 
'./DataSamples/CF-Data-Set-SelTime.img', 
'./DataSamples/CF-Data-Set-P-On.img', 
'./DataSamples/CF-Data-Set-Vol-AttractVol.img', 
'./DataSamples/CF-Data-Set-Force.img', 
'./DataSamples/Free.img', 
'./DataSamples/CF-Data-Set-Vol-Rumble.img', 
'./DataSamples/CF-Data-EnNet.img', 
'./DataSamples/CF-Data-Set-SelTime-CONTINUE.img', 
'./DataSamples/CF-Data-Set-FreeLimit-per.img', 
'./DataSamples/CF-Data-Set-P-All.img', 
'./DataSamples/CF-Data-Set-SelTime-BOAT.img', 
'./DataSamples/CF-Data-Set-Vol-Calibration.img', 
'./DataSamples/CF-Data-NetID-Edit.img', 
'./DataSamples/CF-Data-Set-TrackTwo.img', 
'./DataSamples/CF-Data-Set-Wait-Op.img'
]
		
# User defined options		
				
cmos_img_offset = 0x75BE663		# Image offset of first byte in first occourance of CMOS area on CF card
#cmos_img_offset = 0x75EE663	# Image offset of first byte in second occourance of CMOS area on CF card

#cmos_area_length = 0x147A		# Measured length of one of the duplicated cmos data section
cmos_area_length = 0x1500		# Measured length plus some padding
#cmos_area_length = 0x0F		# DEBUG: Force small problem space

# Checksum algorithm settings
checksum_algorithm = 'SUM16'
checksum_endian = 'little'
checksum_seed = 0x00000000

match checksum_algorithm:
	case 'SUM8':
		checksum_byte_width = 1
	case 'SUM16':
		checksum_byte_width = 2
	case 'SUM24':
		checksum_byte_width = 3
	case 'SUM32':
		checksum_byte_width = 4
	case _:
		sys.exit("Unknown checksum algorithm {}".format(checksum_algorithm))

# Offset in image of suspected checksum (first byte if larger than SUM8)
checksum_candidate_offsets = [0x75BE66F,	# Checksum 1
							  0x75EE66F,	# Checksum 2
							  0x75BE6CB		# Byte in track diff, should be same in most files, use for testing
							 ]
suspected_checksum_offset = checksum_candidate_offsets[0] + 2

#suspected_checksum_offset = int(sys.argv[1],0)

progress_display_interval = 5

DEBUG = False

# ==============================================================================

print("================================================================================")
print("Hydro Thunder CMOS data checksum brute force finder 0.2a")
print("================================================================================\n")

print("Checking CMOS area has correct offset in all .img files")
verifyImageHeaders(cmos_image_paths, cmos_img_offset)

print()

num_comparison = 0
progress_display_last = time.monotonic()

suspected_checksum_bytes = readChecksum(cmos_image_paths[0], suspected_checksum_offset, checksum_algorithm)
# checksum_p_bytes = bytearray(b'\x00\x00\x00\x9c')			# DEBUG: Force user defined checksum to check comparison works
print("About to search for continuous areas in [" + cmos_image_paths[0] + "] CMOS data with a " + checksum_algorithm + " checksum matching : [" + suspected_checksum_bytes.hex(' ') + "]")

input("Press <Enter> to start brute force search...")

time_search_start = time.monotonic()

this_image_path = cmos_image_paths[0]

with open(this_image_path, "rb") as f_p:			
	
	print("       |      Checksum Space     |")
	print("       |   Start    →    Stop    |    Span    | Data | Matching checksums in images")
	
	# Outer loop, determines start offset of bytes being checksumed
	for this_start_offset in range(cmos_img_offset, cmos_img_offset + cmos_area_length, 1):	
		# Inner loop, determines number of bytes (length) being checksumed (reported end byte offset reported by calculateChecksum())
		for this_checksum_length in range(checksum_byte_width, cmos_area_length, checksum_byte_width):
					
			# Call calculateChecksum() to do the checksum (this doesn't add 1 byte at a time but redoes the entire thing every loop, it's much slower but easier to work with)
			checksum_bytes, checksum_start_offset, checksum_end_offset, num_sums, last_byte = calculateChecksum(this_image_path, this_start_offset, this_checksum_length, checksum_algorithm, checksum_endian, checksum_seed)
				
			# Compare if checksumed area results in the same as this image's suspected checksum bytes
			if checksum_bytes == suspected_checksum_bytes:
				print("{:6s} | 0x{:8s} → 0x{:8s} | {:10d} |  {:2s}  | #0 {:s} ".format(checksum_algorithm, checksum_start_offset.to_bytes(4,'big').hex(), checksum_end_offset.to_bytes(4,'big').hex(), num_sums, last_byte.hex(), checksum_bytes.hex(' ')), end='')
			
				this_checksum_matches = 0
				
				# Check if this checksum works in other image files, if so pause, if no keep searching
				for other_image_path_index in range(1, len(cmos_image_paths)):
					other_checksum_bytes, _, _, _, _ = calculateChecksum(cmos_image_paths[other_image_path_index], this_start_offset, this_checksum_length, checksum_algorithm, checksum_endian, checksum_seed)
					
					other_suspected_checksum_bytes = readChecksum(cmos_image_paths[other_image_path_index], suspected_checksum_offset, checksum_algorithm)
					
					if other_checksum_bytes == other_suspected_checksum_bytes:
						print(" | #{:d} {:s}".format(other_image_path_index, other_checksum_bytes.hex(' ')), end='')
						this_checksum_matches += 1
						
				if (this_checksum_matches >= (len(cmos_image_paths) - 1)):
					input("\nMatch found across all images! Press <Enter> to continue brute force search... ")
				
				print()
			elif DEBUG:
				print("{:6s} | 0x{:8s} → 0x{:8s} | {:10d} |  {:2s}  |    {:s}".format(checksum_algorithm, checksum_start_offset.to_bytes(4,'big').hex(), checksum_end_offset.to_bytes(4,'big').hex(), num_sums, last_byte.hex(), checksum_bytes.hex(' ')))
		
			# Print so progress info every x seconds so user can track progress
			if (progress_display_last + progress_display_interval) <= time.monotonic():
				progress = (this_start_offset - cmos_img_offset)/(cmos_area_length)
				time_elapsed = time.monotonic()-time_search_start
				print("{:6s} | 0x{:8s} → 0x{:8s} | {:10d} |  {:2s}  |    {:s}      | Search Space: ~{:7.3f}% complete | {:.0f} s elapsed".format(checksum_algorithm, checksum_start_offset.to_bytes(4,'big').hex(), checksum_end_offset.to_bytes(4,'big').hex(), num_sums, last_byte.hex(), checksum_bytes.hex(' '), progress*100, time_elapsed))
				progress_display_last = time.monotonic()
		
		
		
print('\n Done.\n')

