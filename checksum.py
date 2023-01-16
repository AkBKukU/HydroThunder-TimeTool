#!/usr/bin/python3

import sys
import os
import struct
import datetime
import csv

filename=sys.argv[1]
checksum=0
print ("opening: " + str(filename))

with open(filename, "rb") as f:
    while (byte := f.read(1)):
        #f.seek(score_pos) # Seek to first initial in filename
        val=int.from_bytes( byte, "big")
        if val:
            checksum+=val
            print(hex(checksum))
