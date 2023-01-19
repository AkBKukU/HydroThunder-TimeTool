#!/usr/bin/python3

import sys
import os
import struct
import datetime
import csv
import argparse

parser = argparse.ArgumentParser(
    prog = 'Hydro Thunder Time Tool',
    description = 'Reads and writes data for track times, split times, and'+ 
    'settings for a Hydro Thunder Arcade machine\'s hard drive.',
    epilog = 'Hey, you found a secret!')

parser.add_argument('filename', nargs='?')

# Primary function parameters
parser.add_argument('-t', '--times',action='store_true',
                    help='High score times for tracks')
parser.add_argument('-s', '--splits',action='store_true',
                    help='Best checkpoint split times for tracks')
parser.add_argument('-c', '--config',action='store_true',
                    help='Configuration options and calibration data')
parser.add_argument('-r', '--read', default=None,
                    help='Drive or image to read from')
parser.add_argument('-w', '--write',
                    help='Write data to provided drive or image')
parser.add_argument('--block', default=0,choices=[0,1], type=int,
                    help='Override which data block to read')
parser.add_argument('--write_raw', default=None,
                    help="Write raw data block instead of at end of drive")

# Helpful info options
parser.add_argument('-b', '--boats',action='store_true',
                    help='List boat names in game\'s stored order')
parser.add_argument('-m', '--map_names',action='store_true',
                    help='List track names in game\'s stored order')
# Run argument parsing
args = parser.parse_args()

class ht:
    boats={
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
    iboats = {name: boat_id for boat_id, name in boats.items()}

    
    tracks={
        0:"Ship Graveyard",
        10:"Lost Island",
        20:"Venice Canals",
        30:"Lake Powell",
        40:"Arctic Circle",
        50:"Nile Adventure",
        60:"N.Y. Disaster",
        70:"Greek Isles",
        80:"The Far East",
        90:"TEST - Not Accessible",
        100:"Thunder Park",
        110:"Hydro Speedway",
        120:"Castle Von Dandy - Not Accessible",
        130:"End"
    }

    class data:
        start_offset = [530432,333824] # In bytes from true end of drive
        size = 8192 # Rough size rounded up to nice number
        header = bytearray(b'\x01\x00\x00\x00\x98\xba\xdc\xfe') # Always present
        checksum_offset = 12 # Bytes from data start to checksum
        checksum_seed=0xFEDCBA94 + 1 # +1 to LSB for now until better understood
        config_offset=20
        times_offset=380
        split=offset=1424
        audit_offset=1684


if args.boats:
    for boat in ht.iboats:
        print(boat)
    sys.exit(0)


if args.map_names:
    for key, track in ht.tracks.items():
        print(track)
    sys.exit(0)


class Drive:
    # Object for wrapping a drive, disk image, or raw data block
    def __init__(self, filename):
        self.filename = str(filename) # May be filepath, drive block device, or raw
        self.size = int(os.path.getsize(self.filename))
        self.raw = False if self.size > ht.data.size else True

        self.blocks = [ self.size - ht.data.start_offset[0] if not self.raw else 0 ,
                self.size - ht.data.start_offset[1] if not self.raw else 0]

    def read_times(self):
        times=None


def checksum_calc(drive):
    with open(drive.filename, "rb") as f:
        f.seek(drive.blocks[args.block])
        header = f.read(8)

        if (header == ht.data.header):
            print("PASS : Found [{}] @ {}".format(header.hex(' '), hex(drive.blocks[args.block])))

        f.read(4)
        checksum_stored=f.read(4)
        f.read(4)

        checksum=ht.data.checksum_seed
        int_read=int(ht.data.size/4)
        for count in range(int_read):
            next_int_bytes = f.read(4)
            next_int = int.from_bytes(next_int_bytes, "little", signed=False)
            checksum = (checksum+next_int) % 0xFFFFFFFF # Use mask to force overflow
        
        print("Checksum:")
        print("Found: {}".format(checksum_stored.hex(" ")))
        print("Sumed: {}".format(checksum.to_bytes(4,"little", signed=False).hex(" ")))

        return checksum.to_bytes(4,"little", signed=False).hex(" ")




if args.read is not None:
    read_drive = Drive(args.read)

    # Add else to use write drive as read if data CSV provided
else:
    read_drive = None

if args.write_raw is not None:
    write_filename=args.write_raw
    with open(read_drive.filename, "rb") as r:
        with open(write_filename, "wb") as w:

            # Seek to block
            r.seek(read_drive.blocks[args.block])
            print("Reading: {}".format(hex(read_drive.blocks[args.block])))
            for position in range(ht.data.size):
                # Add options to replace data from CSV based on position
                w.write(r.read(1))

    



sys.exit(0)

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
