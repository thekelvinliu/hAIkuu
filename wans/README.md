# Word Association Norms (WAN)
The haiku generation algorithm used in this project relies on a directed graph of words.
In this graph, each node represents a particular word.
An edge is drawn between two nodes if the corresponding words are related.
Word relationships are determined by word association norms, and this project uses [Free Association Norms](http://w3.usf.edu/FreeAssociation/AppendixA/index.html) from the University of South Florida.
The direction of an edge is determined by which word is the _cue_ and which is the _target_.
Edges always go from _cue_ to _target_.
See the above link for more detailed information.

This project uses `cue_targets_mapping.json` to represent the graph.
This file maps a single word (the _cue_) to a list of other words (the _targets_).
A convenience script is included to download files from USF and generate `cue_targets_mapping.json`.
To run, open a terminal in the root of this project and execute the following:
```
$ cd wans
$ ./generate_map.sh
```
