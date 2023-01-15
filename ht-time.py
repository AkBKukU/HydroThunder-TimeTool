#!/usr/bin/python3

import sys
import os
import struct
import datetime
import csv

filename=sys.argv[1]

data_csv=None
if len(sys.argv) > 2:
    data_csv=sys.argv[2]

# Sample file size 4000317440
data_size=123993699 # measured by checking for 0'ed out portion of drive after loading game on new drive

size=os.path.getsize(filename)

# This offset does not appear to be consistent across machines/versions
scores_start=[size-333444,size-530052]

boat_LUT= {
    b'\x00':"Banshee",
    b'\x01':"Tidal Blade",
    b'\x02':"Rad Hazzard",
    b'\x03':"Miss Behave",
    b'\x04':"Damn the Torpedoes",
    b'\x05':"Cutthroat",
    b'\x06':"Razorback",
    b'\x07':"Thresher",
    b'\x08':"Midway",
    b'\t':"Chumdinger",
    b'\n':"Armed Response",
    b'\x0b':"Blowfish",
    b'\x0c':"Tinytanic"
}

inverse_boat_lut = {name: boat_id for boat_id, name in boat_LUT.items()}

# Hidden track names extracted from disk image offset 0xAC6F860 (archive.org-HydroThunder-1.00d.img) [CRC32: 39205D83]
# Data at offset also suggests possibly another removed track "T.TWAT1" (no high score data for it)
track_order={
    0:"Ship Graveyard",
    10:"Lost Island",
    20:"Venice Canals",
    30:"Lake Powell",
    40:"Arctic Circle",
    50:"Nile Adventure",
    60:"N.Y. Disaster",
    70:"Greek Isles",
    80:"The Far East",
    90:"TEST",
    100:"Thunder Park",
    110:"Hydro Speedway",
    120:"LOOP3",
    130:"End"
    }

time = ""
for score_pos in scores_start:
    scores=0
	
	# Write data
    if data_csv:
        with open(filename, "r+b") as f:
            f.seek(score_pos) # Seek to first initial in filename
            with open(data_csv, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    timedelta = datetime.datetime.strptime(row['Time'], "%M:%S.%f") - datetime.datetime(1900,1,1)

                    f.write(inverse_boat_lut[row['Boat']])
                    f.write(row['Initials'].encode("ascii"))
                    f.write(struct.pack('<f', timedelta.total_seconds()))
	
	# Read data
    else:
        print ("")
        print ("-------------------------------------------------------")
        print ("Track Leaderboard Entries")
        with open(filename, "rb") as f:
            f.seek(score_pos) # Seek to first initial in filename
            with open(filename+".csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["Track","Initials","Boat","Time"])

                while scores < 130:
                    if (scores % 10 == 0):
                        print ("-------------------------------------------------------")
                    boat = f.read(1) # read boat
                    #print (boat_LUT[boat])
                    initials = str(f.read(3),"ascii") # read initials
                    #print (initials)
                    time = f.read(4) # read four bytes for float representing time in seconds
                    # Note: Game rounds weirdly and these results may differ
                    timestamp=str(datetime.timedelta( seconds=round(struct.unpack('<f', time)[0],2) ))[2:][:8]
                    writer.writerow([track_order[scores-(scores % 10)],initials,boat_LUT[boat],timestamp])
                    print("{:15s} | {:3s} | {:20s} | {:8s}".format(track_order[scores-(scores % 10)], initials, boat_LUT[boat], timestamp))
                    scores=scores+1
                    
                print ("")
                print ("-------------------------------------------------------")
                print ("Track Personal Best Split Time Entries")
				
                _ = f.read(4) # discard unknown word, maybe a terminator, have to check if it changes
                    
                timesplit = 0
                track = -10
                while timesplit < 65:
                    if (timesplit % 5 == 0):
                        print ("-------------------------------------------------------")
                        track = track + 10
                    splittime = f.read(4) # read four bytes for float representing time in seconds
                    formattedsplit=str(datetime.timedelta( seconds=round(struct.unpack('<f', splittime)[0],2) ))[2:][:8]
                    if formattedsplit == "03:45.67":
                        unusedflag = "UNUSED"
                    else:
                        unusedflag = ""
                    checkpointnum = (timesplit % 5) + 1
                    print("{:15s} | {:1d} | {:8s} | {}".format(track_order[track], checkpointnum, formattedsplit, unusedflag))
                    timesplit=timesplit+1
