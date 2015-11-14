# Word Association Norms (WAN)
Word association norms are used to choose word for each haiku.
This project uses [Free Association Norms](http://w3.usf.edu/FreeAssociation/AppendixA/index.html) from the University of South Florida.
To download, run
```
$ ./download.sh
```
from the `./data/wans` directory.
Then, transform the data with
```
./clean.py
```
This will generate a file called `cue_target_pairs.json`, which contains the data this project uses to generate haikus.
