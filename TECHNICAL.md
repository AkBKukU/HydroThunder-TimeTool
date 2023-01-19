# Technical Details of How Data Is Stored

Hydro Thunder's Arcade version is run in a fairly typical PC. The game is stored
on two partitions of a hard drive. A third partition exists that is empty, 
potentially for future use that never happened.

However, the game stores modifiable data in a non-PC method. All modifiable data
(which includes High Scores, Split Times, Audit Logging, Operator Settings, 
and Calibration Values) is stored raw on the drive. Internally the game
references this data as "CMOS" but it is not stored in any kind of static
memory like that, it only exists on the hard drive.

## Location Of Data

The position of this starts at 1,036 512 byte sectors (530,432 bytes total) from
the end of the drive. There does not seem to be a definitive end to the data, 
possibly due to the structure. It does fit within 65,536 bytes comfortably. 
There is a second identical *type* of data 384 sectors after the first set. 
Based on how the machine works, these are redundant sets of data that are
written either sequentially to be identical or alternating in case the machine 
is turned off during a write.

## Structure Of Data

The data is stored in distinct sections for different sources. Below is the 
structure with by sizes for v1.01b of the game. v1.00d is similar but missing
some settings.

### Header (20 bytes)

The header area contains some static data that does not change and the checksum.

### Settings and Calibration (360 bytes)

Next are all of the values set in the Operator Menu for the game. The majority
of the settings are stored a 32b int values but some are stored as 32b floats.

### High Scores / Best Times (1040 bytes)

High scores have three components stores in 8 bytes:
 - [1 byte] The boat used
 - [3 bytes] The initials of the player
 - [4 bytes] Total time as a float of seconds

Each track stores 10 scores and there are 13 tracks worth of data (there are two
unused tracks in the game).

### Split Times (260 bytes)

Each of the 13 tracks have 5 split times for checkpoints stored as 4 byte 
floats. Not all values are used as not all tracks have 5 checkpoints. Split
times appear to be total time, not time between checkpoints.

### Audit Data (1680? bytes)

All data after split times appears to be audit data. No effort has been made to
map this data as the game itself has the ability to export it to a text file on
a floppy disk from the operator menu. The exact size of this data is not 
confirmed, it doesn't come close to filling the space between the first and 
second copies of data nor does it align with any common sizes. On a drive taken 
from a machine with considerable play time the last byte was 1680 bytes away 
from the start and has been used as a rough estimate.


## Checksum

The data stored is validated by the game on start up by using a checksum. If
the data does not match the checksum the machine will revert to factory defaults
and clear audit data. 

To calculate the checksum, first clear the existing checksum from the data. The 
add up all the values in the data as 32b ints. The checksum has a starting value
of 0xFEDCBA94 the other bytes are added to.





