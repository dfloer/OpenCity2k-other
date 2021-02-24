# Streets .scn file spec:

Warning, this is more or less rough notes right now.

## Header

Starts with `MIFF`, 2 and then `SCED` and `STCS` chunk names.
Note that all chunk names (**except MIFF**) are reversed in the .scn file. So STCS is actually CSTS.

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
|ITXT|-|N||
|WANM|1B|N||
|WTXT|-|N||
|LANM|1B|N||
|LTXT|-|N||
|PRGN|4B|N||
|#AIS|4B|N|Number of AI cars|
|ANAI|48B|Y|Data related to AIs, there will be an equal number here to #AIS|
|#EVS|4B|N||
|EVNT|?|Y|Events. Count equal to #EVS.|
|LABL|?|N|Label?|
|#CHK|4B|N|Number of checkpoints|
|CHCK|4B|Y|(x, y) coordinate pair for the checkpoints. Same number of entries as #CHK.|
|EPSD|24B|N||
|#PKG|4B|N|# of packages|
|APAK|?|Y|Package info. Count equal to #PKG|
|EVTG|?|Y|Unknown|


## Subsections

### LABL

Contains data entries for labels.

### ANAI

AI data, exact contents currently undetermined.
Difficulty changes in editor reflected here.

### EPSD

Unknown.

### APAK

Data related to the package. At minimum, contains text and a sound to play.

### EVNT

Events. Rewards stored here.

### EVTG

Unknown.

## Notes

No compression!