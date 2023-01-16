#!/usr/bin/python3

# This script attempts to brute force the start and end offsets for suspected checksums in the Hydro Thunder CMOS data. Currently only very basic SUM8, SUM16, SUM24 and SUM32 are implemented and tested. 

import sys
import os
import struct
import datetime

cmos_primary_image_path = './DataSamples/SN33-Real.img'

cmos_secondary_image_path = [ './DataSamples/Pay.img',
							'./DataSamples/Free.img',
							'./DataSamples/CF-Data-AIDiff-Big.img',
							'./DataSamples/CF-Data-AIDiff.img',
							'./DataSamples/CF-Data-EnNet.img',
							'./DataSamples/CF-Data-HS.img',
							'./DataSamples/CF-Data-HS-LS.img',
							'./DataSamples/CF-Data-NetID.img'
							]

cmos_img_offset = 0x75BE663		# Default offset for CF card first occourance
#cmos_img_offset = 0x75EE663	# Default offset for CF card second occurrence

#cmos_area_length = 0x147A		# Measured length of one of the duplicated cmos data section
cmos_area_length = 0x1500		# Measured length plus some padding
#cmos_area_length = 0x0F		# DEBUG: Force small problem space

checksum_candidate_offset = [0x75BE66F			# Checksum suspected to be for operator settings, changed with track/ai diff, observed overflow into this byte, likely 2 byte or 4 byte
							 ]
							 
suspected_checksum_offset = checksum_candidate_offset[0]

checksum_num_bytes = 2
# TODO: Change byte mask in software, YOU HAVE TO DO IT MANUALLY (the 0xFFFF things must match your num bytes)

# ==============================================================================

def verifyImageHeaders(image_path_list, cmos_img_offset):
	for this_file in range(len(image_path_list)):
		with open(image_path_list[this_file], "rb") as f:
			# Seek to first byte, next DWORD is (01 00 00 00)
			f.seek(cmos_img_offset)
			cmos_header = bytearray()
			cmos_header += f.read(1)
			cmos_header += f.read(1)
			cmos_header += f.read(1)
			cmos_header += f.read(1)
			
		if (cmos_header == bytearray(b'\x01\x00\x00\x00')):
			print("  Image #{:2d} PASS : Found [01 00 00 00]   [{:s}]".format(this_file,image_path_list[this_file]))
			
		else:
			sys.exit("  Image #{:2d} PASS : Found [01 00 00 00]   [{:s}]".format(this_file,image_path_list[this_file]))

def verifyImageChecksum(image_path, expected_checksum, checksum_num_bytes, checksum_offset, checksum_data_offset_start, checksum_length):
	checksum_sum = 0
	
	with open(image_path, "rb") as f_s:					
		f_s.seek(suspected_checksum_offset)
		checksum_s_bytes = f_p.read(checksum_num_bytes)
		
		f_s.seek(checksum_data_offset_start)
		
		for j in range(checksum_length + 1):
			this_byte = f_s.read(1)
			
			this_byte_int = int.from_bytes(this_byte, 'big', signed=False)
			checksum_sum = (this_byte_int + checksum_sum) % 0xFFFF
			checksum_sum_bytes = checksum_sum.to_bytes(checksum_num_bytes,'big', signed=False)
			
	print(" " + checksum_sum_bytes.hex(' ') + " |", end='')
	
	return (checksum_sum_bytes == expected_checksum)

# ==============================================================================

print()

print("Checking cmos area has correct offset in .img files")
verifyImageHeaders([cmos_primary_image_path] + cmos_secondary_image_path, cmos_img_offset)

print()

num_comparison = 0

with open(cmos_primary_image_path, "rb") as f_p:		
	f_p.seek(suspected_checksum_offset)
	checksum_p_bytes = f_p.read(checksum_num_bytes)
	# checksum_p_bytes = bytearray(b'\x00\x00\x00\x9c')			# DEBUG: Force user defined checksum to check comparison works
	print("About to search for continuous areas in cmos data with a checksum with <algorithm> matching : [" + checksum_p_bytes.hex(' ') + "]")
	
	input("Press <Enter> to start brute force search...")
		

	# Start brute forcing checksum
	
	traverse_start_offset = f_p.tell()
	
	print("           |      Checksum Space     |             |                   ")
	print("  Ops      |   Start    →    Stop    |    Span     | Data | Checksums  ")
	
	for this_start_offset in range(cmos_area_length):
	
		checksum_sum = int(0)
	
		checksum_offset_start = traverse_start_offset + this_start_offset
		f_p.seek(checksum_offset_start)
		traverse_length = cmos_area_length - this_start_offset
		
		for pos_p in range(traverse_length):
			checksum_offset_end = f_p.tell()
			this_byte = f_p.read(1)
			
			this_byte_int = int.from_bytes(this_byte, 'big', signed=False)
			checksum_sum = (this_byte_int + checksum_sum) % 0xFFFF
			checksum_sum_bytes = checksum_sum.to_bytes(checksum_num_bytes,'big', signed=False)
			
			num_comparison += 1
			
			# Disabling the cli output will speed up the brute force
			#print( "\n {:15d} | ".format(num_comparison) + "0x" + checksum_offset_start.to_bytes(4,'big').hex() + " → 0x" + checksum_offset_end.to_bytes(4,'big').hex() + " |  " + this_byte.hex(' ') + "  | " + checksum_sum_bytes.hex(' ') + " | ", end='')
			
			if checksum_sum_bytes == checksum_p_bytes:
				# Found possible checksum for data
				print( "\n{:10d} | ".format(num_comparison) + "0x" + checksum_offset_start.to_bytes(4,'big').hex() + " → 0x" + checksum_offset_end.to_bytes(4,'big').hex() + " |  " + "{:10d}".format(checksum_offset_end-checksum_offset_start) + " |  " + this_byte.hex(' ') + "  | " + checksum_sum_bytes.hex(' ') + " | ", end='')
				#print (" Primary: PASS", end='')
				
				#cmos_secondary_image_path[1] = cmos_primary_image_path		# DEBUG: Force use same file for secondary matches, should always pass 2nd match
				
				secondary_mismatch = 0
				secondary_image_index = 0
				
				while not(secondary_mismatch) and secondary_image_index < len(cmos_secondary_image_path):

					if verifyImageChecksum(cmos_secondary_image_path[secondary_image_index], checksum_sum_bytes, checksum_num_bytes, suspected_checksum_offset, checksum_offset_start, pos_p):
						pass
						#print(" → Secondary #" + str(secondary_image_index + 1) +": PASS", end='')
					else:
						print(" → Secondary #" + str(secondary_image_index + 1) +": FAIL", end='')
						secondary_mismatch = 1
					
					secondary_image_index += 1
					if secondary_image_index > 7:
						input(" Match found across all images! Press <Enter> to continue brute force search...")
									
print('\n Done.\n')
