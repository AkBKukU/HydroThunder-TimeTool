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

## Roadmap
 - More documentation of hidden data
 - Provide exmaples of data
 - Determine how data validity check is done and impliment it for modified scores
