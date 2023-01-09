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
    90:"Unknown 1",
    100:"Thunder Park",
    110:"Hydro Speedway",
    120:"Unknown 2",
    130:"End"
    }

time = ""
for score_pos in scores_start:
    scores=0
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

    else:
        with open(filename, "rb") as f:
            f.seek(score_pos) # Seek to first initial in filename
            with open(filename+".csv", 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["Track","Initials","Boat","Time"])

                while scores < 130:
                    #if (scores % 10 == 0):
                        #print (track_order[scores])
                    boat = f.read(1) # read boat
                    #print (boat_LUT[boat])
                    initials = str(f.read(3),"ascii") # read initials
                    #print (initials)
                    time = f.read(4) # read four bytes for float representing time in seconds
                    # Note: Game rounds weirdly and these results may differ
                    timestamp=str(datetime.timedelta( seconds=round(struct.unpack('<f', time)[0],2) ))[2:][:8]
                    writer.writerow([track_order[scores-(scores % 10)],initials,boat_LUT[boat],timestamp])
                    print("\""+track_order[scores-(scores % 10)]+"\",\""+initials +"\", \"" + boat_LUT[boat] +"\", " +timestamp)
                    scores=scores+1
