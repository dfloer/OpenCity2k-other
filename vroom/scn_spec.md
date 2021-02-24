# Streets .scn file spec:

Warning, this is more or less rough notes right now.

## Header

Starts with `MIFF`, 2 and then `SCED` and `STCS` chunk names.
Note that all chunk names (**except MIFF**) are reversed in the .scn file. So STCS is actually CSTS.


## Chunks

General format is the chunk name (4B), length of the chunk (4B) which is inclusive of the name and length, and then the chunk data.

|Chunk Name|Length (- for variable) | Multiple | Notes |
|-|-|-|-|
|CITY|-|N|Name of the .sc2 file to load.|
|NAME|-|N|Race Title|
|TIME|4B|N|Time Limit (seconds)|
|CHKB|4B|N|Checkpoint time bonus (seconds)|
|BNUS|4B|N||
|LOCX|4B|N||
|LOCY|4B|N||
|PACK|4B|N||
|AMMO|4B|N||
|LAPS|4B|N|How many laps.|
|IANM|1B|N||
|ITXT|-|N|Intro Text - description text on mission selection screen.|
|WANM|1B|N||
|WTXT|-|N|Win Text?|
|LANM|1B|N||
|LTXT|-|N|Loss Text?|
|PRGN|4B|N||
|#AIS|4B|N|Number of AI cars|
|ANAI|48B|Y|Data related to AIs, there will be an equal number here to #AIS|
|#EVS|4B|N||
|EVNT|?|Y|Events. Count equal to #EVS.|
|LABL|-|N|Location labels in the game.|
|#CHK|4B|N|Number of checkpoints|
|CHCK|4B|Y|(x, y) coordinate pair for the checkpoints.|
|EPSD|24B|N||
|#PKG|4B|N|# of packages|
|APAK|?|Y|Package info. Count equal to #PKG|
|EVTG|14B|Y|Unknown|

## Subsections

### LABL

Contains data entries for location labels. Unknown where the number of entries comes from, otherwise, there are strings seperated by a lot of `0x01` bytes. Also unknown how they get triggered.

### ANAI

AI data, exact contents currently undetermined.
Difficulty changes in editor reflected here.

### EPSD

Unknown.

### APAK

Data related to the package. At minimum, contains text indicating what to do with the package and a sound to play.

5x4B of of data to start:

|0|1|2|3|4|
|-|-|-|-|-|
|id|Bonus|?|?|?|

At least 0 and 1 have a bonus attached to them.

Then text and wav files to play as appropriate.


### EVNT

Events. Rewards stored here.
Always seems to end with `CD CD CD CD` when present.

Looks to be a first part of 8 numbers, and then strings/wav files as appropriate.

Possible format (each is 4B int32):

|0|1|2|3|4|5|6|7|
|-|-|-|-|-|-|-|-|
|id|bonus points multiplier|additional time (seconds)|Additional $|?|?|?|?|

id 999 is special and to do with levels?

### EVTG

Unknown. `CD CD` ending, padding?

### CHCK

Contains the (X, Y) coordinate to the city file for the checkpoints.
Same number of entries as #CHK. Races need at least one checkpoint.

## Notes

No compression!
