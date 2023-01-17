#!/usr/bin/python3

# This script contains the fuctions called in other HTchecksum scripts.

import sys
import os
import struct
import datetime
import math

DEBUG = False

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
			# TODO: Add extra 98 BA DC FE
			
		if (cmos_header == bytearray(b'\x01\x00\x00\x00')):
			print("  Image #{:2d} PASS : Found [01 00 00 00]   [{:s}]".format(this_file,image_path_list[this_file]))
			
		else:
			sys.exit("  Image #{:2d} FAIL! : Expected [01 00 00 00] but found [{}] !  [{:s}]".format(this_file, cmos_header.hex(' '),image_path_list[this_file]))

def calculateChecksum(checksum_algorithm, checksum_endian, image_path, checksum_start_offset, checksum_length_bytes, checksum_seed = 0x00000000):

	match checksum_algorithm:
		case 'SUM8':
			checksum_byte_width = 1
			checksum_mask = 0xFF
			checksum_length_reads = checksum_length_bytes
		case 'SUM16':
			checksum_byte_width = 2
			checksum_mask = 0xFFFF
			checksum_length_reads = checksum_length_bytes / checksum_byte_width
			if checksum_length_reads != int(checksum_length_reads):
				sys.exit("Checksum data length mismatch with algorithm, length must be multiple of checksum byte width '{}'".format(checksum_byte_width))
		case 'SUM24':
			checksum_byte_width = 3
			checksum_mask = 0xFFFFFF
			checksum_length_reads = checksum_length_bytes / checksum_byte_width
			if checksum_length_reads != int(checksum_length_reads):
				sys.exit("Checksum data length mismatch with algorithm, length must be multiple of checksum byte width '{}'".format(checksum_byte_width))
		case 'SUM32':
			checksum_byte_width = 4
			checksum_mask = 0xFFFFFFFF
			checksum_length_reads = checksum_length_bytes / checksum_byte_width
			if checksum_length_reads != int(checksum_length_reads):
				sys.exit("Checksum data length mismatch with algorithm, length must be multiple of checksum byte width '{}'".format(checksum_byte_width))
		case _:
			sys.exit("Unknown checksum algorithm {}".format(checksum_algorithm))
			
	checksum_seed = checksum_seed % checksum_mask
	checksum_length_reads = int(checksum_length_reads)
			
	with open(image_path, "rb") as f_s:						
		f_s.seek(checksum_start_offset)
		
		checksum_sum = checksum_seed
		num_sums = 0
		for this_data_offset in range(checksum_length_reads):
			this_byte = f_s.read(checksum_byte_width)
			num_sums += 1
			
			this_byte_int = int.from_bytes(this_byte, checksum_endian, signed=False)
			checksum_sum = (this_byte_int + checksum_sum) % checksum_mask
			checksum_sum_bytes = checksum_sum.to_bytes(checksum_byte_width,checksum_endian, signed=False)
			
		checksum_end_offset = f_s.tell() - 1
			
	if DEBUG:
		print("\n" + checksum_algorithm + " | 0x" + checksum_start_offset.to_bytes(4,checksum_endian).hex() + " → 0x" + (checksum_end_offset).to_bytes(4,checksum_endian).hex() + " |  " + "{:10d}".format(num_sums) + " |  " + this_byte.hex(' ') + "  | " + checksum_sum_bytes.hex(' ') + " | ")
			
	last_byte = this_byte
			
	return checksum_sum_bytes, checksum_start_offset, checksum_end_offset, num_sums, last_byte

def getChecksum(checksum_algorithm, image_path, checksum_offset):

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
			sys.exit("Unknown checksum algorithm '{}'".format(checksum_algorithm))

	with open(image_path, "rb") as f_s:					
		f_s.seek(checksum_offset)
		checksum_bytes = f_s.read(checksum_byte_width)

	return checksum_bytes
