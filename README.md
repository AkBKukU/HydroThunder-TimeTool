# HydroThunder-TimeTool
Tool for exporting and importing high score times from Hydro Thunder Arcade as CSV files. This program works with a *full* drive image, not CHD or just files. The high score data is not stored as a normal file and only exists as raw data at the end of the drive.

**WARNING - THIS MAY CAUSE A FACTORY RESET OF YOUR MACHINE WIPING SCORES, SETTINGS, AND AUDIT DATA**

## Usage

First, image your HDD. If you are using linux a simple `dd` image will do:
```
dd if=/dev/sd[letter here] of=./HT-HDD.img
```
Make a **backup** of this file, this is not a perfect process and the game will reset all data when things go wrong.

To read high score times run the program with the drive image as a parameter:
```
python3 ./ht-time.py ./HT-HDD.img
```

It will create a `HT-HDD.img.csv` file with all the high scores extracted.

To write high score times back to the drive image run the program with the drive image and CSV as a parameters:
**!!NOT YET USABLE FOR REAL!!**
```
python3 ./ht-time.py ./HT-HDD.img  ./HT-HDD.img.csv
```
**NOTE:** Currently this version can write times back to the game but they fail a validity check and the machine resets to factory defaults.

You can then image the drive back but it would be better to only write the score data. A `dd` like with `seek` and `skip` can do this.

TODO - provide example

## "CMOS" Data area details
The data area that contains the high score table is towards the end of the HDD in an unformatted area, is internally referred to as "cmos" in _HYDRO.EXE_ (1.00d). This CMOS area also contains other data that has not yet been decoded. 

This data (or a checksum of it) may also be stored in the PC motherboard battery backed CMOS memory and flushed periodically to the non-volatile HDD, further reverse engineering required to determine this.

### Known CMOS data pointers from decompiling _HYDRO.EXE_ (1.00d) and current script support
| Offset  | Internal Game Name         | Decoded      | CSV export | Write back |
|---------|----------------------------|--------------|------------|------------|
| 62B300h | \_OperatorSettings         | No           | No         | No         |
| 622640h | \_Hi_Score\_Table          | **Yes**      | **Yes**    | Partial    |
| 622A50h | \_Hud\_SplitTimes          | **Yes**      | No         | No         |
| 6221FCh | \_Diagnos\_DiagnosticInfo  | No           | No         | No         |
| 620C18h | \_Audits\_Data             | No           | No         | No         |
| 62091Ch | \_AiRabbit\_WinHistoryData | No           | No         | No         |

### Data structure maps

#### CMOS area structure (1.00d)

```
Offset (1.00d)| Description 
--------------|--------------------------------------------------------------------------------------------------------
0000h         | Start of CMOS area (01 00 00 00 98 BA DC FE 01)
0000h - 0063h | Unknown, some changes between 1.00d & 1.01b, suspect settings
0064h - 0097h | Track difficultly
0098h - 00CBh | AI difficultly
00CCh - 016Fh | Unknown, significant change between versions (extra 11 bytes in 1.01b offseting all later data!)
0170h - 057Fh | Hi_Score_Table
0580h - 0583h | Unknown DWORD, no change between versions, maybe just a terminator (41 00 00 00)
0584h - 0687h | Hud_SplitTimes
0688h - 0733h | Unknown, changes between versions
0734h - 0B1Dh | Unknown block with repeating structure every 108 bytes, much more data in 1.01b
0B1Eh - 0C43h | Empty space (0x00 filled)
0C44h - 0FC0h | Unknown block with repeating structure every 108 bytes, much more data in 1.01b
0FC1h - 146Fh | Unknown, changes between versions
        146Fh | End of CMOS area
```

### Track and AI difficultly
##### Entry structure
```
| diff : uint8 | null (0x00)  | null (0x00)  | null (0x00)  |
|--------------|--------------|--------------|--------------|
| byte 0       | byte 1       | byte 2       | byte 3       |
```

### `Hi_Score_Table`
##### Entry structure
```
| boat : byte |           initials : char[3]            |                seconds : single float                 |
|-------------|-----------------------------------------|-------------------------------------------------------|
| byte 0      | byte 1      | byte 2      | byte 3      | byte 4      | byte 5      | byte 6      | byte 7      |
```
##### Table structure
```
|     'Ship Graveyard' high scores     |       'Lost Island' high scores      | ... |          'LOOP3' high scores         |
|    1st   |    2nd   | ... |   10th   |    1st   |    2nd   | ... |   10th   | ... |    1st   |    2nd   | ... |   10th   |
|0|123|4567|0|123|4567| ... |0|123|4567|0|123|4567|0|123|4567| ... |0|123|4567| ... |0|123|4567|0|123|4567| ... |0|123|4567|
```


### `Hud_SplitTimes`
##### Entry structure
```
|                seconds : single float                 |
|-------------------------------------------------------|
| byte 0      | byte 1      | byte 2      | byte 3      |
```
##### Table structure
```
|'Ship Graveyard' split times |  'Lost Island' split times  | ... |     'LOOP3' split times     |
|Split 1|Split 2| ... |Split 5|Split 1|Split 2| ... |Split 5| ... |Split 1|Split 2| ... |Split 5|
| 0123  | 0123  | ... | 0123  | 0123  | 0123  | ... | 0123  | ... | 0123  | 0123  | ... | 0123  |
```
### Special case notes
* The CMOS data contains data for 2 extra inaccessible tracks 'TEST' and 'LOOP3'.
* Tracks that have less than 5 split check points just leave the extra unused ones with their default time ~225 s (85 AB 61 43).


## Roadmap
- More documentation of hidden data
- Provide exmaples of data
- Determine how data validity check is done and impliment it for modified scores
