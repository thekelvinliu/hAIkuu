# N-grams Data
The haiku generation algorithm used in this project uses n-grams to build each haiku.
This project uses the [Corpus of Contemporary American English](http://www.ngrams.info/samples_coca1.asp) from Brigham Young University.
Please go to their website and download the free files with part of speech.
Extract the zips, and place the resulting 4 text files -- `w{2,3,4,5}c.zip` -- in the `downloads` directory of this directory.
Next, execute the following to create `clean_ngrams.json`.
```
$ ./clean_ngrams.py
```
This will create the file,
This file contains a list of lists.
Each inner list has the form `[ngram, x, y]` where `x` and `y` are the parts of speech tag of the first and last words of the ngram respectively.

Now for the good stuff.
Ensure you have [MySQL](https://www.mysql.com/) installed and running.
Set the environment variables, `` and ``, to the correct credentials.
Finally, run the following:
```
$ ./build_db.py
```
This will create a new database and populate it with a bunch of tables.
It'll take some time, but afterwards, feel free to poke around the database.
When the script completes, all the setup is done!

`build_db.py` is not yet written.
Essentially, it creates a new database in MySQL with this command `CREATE DATABASE IF NOT EXISTS haikuu CHARACTER SET utf8;`
Then, it creates a main ngram table, which has columns for and `nid` (the ngram id), `ngram` (the ngram itself), `first_tag` (the POS tag of the first word), and `last_tag` (the POS tag of the last word).
Rows are populated using the data in `clean_ngrams.json`.
After, it creates a table for each of the cue words with a single column, `nid`.
A particular ngram's `nid` will be in a particular cue word's table if the cue word is anywhere in the ngram.
