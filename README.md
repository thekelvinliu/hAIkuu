# haikuu
an image-based haiku generator
📷🗻🖊😎💯

## Getting Started
This project requires some setup.
First nagivate to the `wans` directory and follow the steps outlined in the readme.
Next, do the same in the `coca` directory.
After these are complete, you should be ready to go!
To start the server, simply do
```
$ ./runserver.py
```
from the root project directory.
Then, open a web browser and nagivate to `http://localhost:5000`.
Have fun!

## Notes
This is a (wip) reimplementation of a previous project created by Henry Du, Kelvin Liu, Shahn Shamdasani, and Andrew Sy.
The project originated as a hackathon hack at [HackHarvard2015](http://hackharvard2015.devpost.com/).
Check out the `hackharvard2015-save` branch to see what was demoed.

This reimplementation has heavier focus on the haiku generation algorithm.
Instead of hold _all_ of the data in memory, [sqlite](https://www.sqlite.org/) is used.
Currently, there is no user interface.
The text seen when visiting the page is simply a random word followed by the haikuu generated from that word.
