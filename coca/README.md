# N-grams Data
The haiku generation algorithm used in this project uses n-grams to build each haiku.
This project uses the [Corpus of Contemporary American English](http://www.ngrams.info/samples_coca1.asp) from Brigham Young University.
Please go to their website and download the free files with part of speech.
Extract the all the zips to a new directory within this one, called `downloads`.
The `downloads` directory should have 4 text files -- `w{2,3,4,5}c.txt`.
Next, execute the following to create `clean_ngrams.json`.
```
$ ./clean_ngrams.py
```
This will output a json file that represents a list of lists.
Each inner list has the form `[ngram, x, y]` where `x` and `y` are the parts of speech tag of the first and last words of the ngram respectively.

Now for the good stuff.
`build_db.py` will go through all this data and create a simple sqlite database.
This database includes a main ngram table, which has columns for `id` (the ngram id), `ngram` (the ngram itself), `first` (the POS tag of the first word), and `last` (the POS tag of the last word).
Rows are populated using the data in `clean_ngrams.json`.
After it creates a table for each of the cue words with a single column, `nid`.
A particular ngram's `nid` will be in a particular cue word's table if the cue word is anywhere in the ngram.
Simply run the following:
```
$ ./build_db.py
```
Note: this process does take quite some time.
The time it takes to finish could potentially be reduced by using a Queue and Threads, but due to CPython's GIL, I decided using a single thread would reduce complexity.
