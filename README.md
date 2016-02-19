# haikuu
an image-based haiku generator
📷🗻🖊😎💯

## Getting Started
First, clone this repository and navigate into the folder.
```
$ git clone https://github.com/thekelvinliu/hAIkuu.git
$ cd hAIkuu
```
Next, create a Python [Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in this directory, and activate it.
Please make sure to use python2.7.
```
$ virtualenv -p python2.7 venv
$ source venv/bin/activate
```
Sometimes when the absolute path to the directory contains spaces, `pip` gest messed up.
Ensure that `pip` is working properly.
```
$ pip list
pip (7.1.2)
setuptools (18.2)
wheel (0.24.0)
```
If you get some sort of bad interpreter error, edit the shebang (`#!`) line in `venv/bin/pip`.
Something like `#!/usr/bin/env python` should work, since you've already activated the virtual env.
Now, install this project's dependencies.
```
$ pip install flask
```
Next, nagivate to the `wans` directory and follow the steps outlined in the readme.
Then, do the same in the `coca` directory.
After these are complete, you should be ready to go!
To start the server, simply do
```
$ ./runserver.py
```
from the root project directory.
Then, open a web browser and nagivate to `http://localhost:5000`.
Have fun!

## Todo
This project is still very much in alpha, and there's so much to improve on.
- handling the data
  - previously, all the data was loaded into memory upon startup, resulting in super _slow_ load times.
  - now, this project handles data using [sqlite](https://www.sqlite.org/).
  - in the future, this may change to [MySQL](https://www.mysql.com/).
- haiku generation algorithm
  - previously, haikuu generation was slow, and a lot of the haikuus didn't make sense.
  - now, the haikuus are generated a lot faster, but still lack consistent results
  - in the future, POS tags will actually be used in the generation algorithm, hopefully resulting in deep and meaningful haikuus every time.
- user interface
  - previously, there was an interactive website allowing users to generate haikuus based on images or text, _but_ this website was super buggy.
  - now, there is no UI -- the text seen is simply a random word followed by the haikuu genereated with that word.
  - in the future, the original website will be brought back, bug-free.

## Notes
This is a (wip) reimplementation of a previous project created by Henry Du, Kelvin Liu, Shahn Shamdasani, and Andrew Sy.
The project originated as a hackathon hack at [HackHarvard2015](http://hackharvard2015.devpost.com/).
Check out the `hackharvard2015-save` branch to see what was demoed.
