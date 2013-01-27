#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: img2txt.py <imgfile> [--size=<size>] [--level=<level>]

"""

from docopt import docopt

dct = docopt(__doc__)

imgname = dct['<imgfile>']

MaxLen = dct['--size']

try:
    MaxLen = float(MaxLen)
except:
    MaxLen = 100.0   # default maxlen: 100px

level = dct['--level']

try:
    level = float(level)
except:
    level = 10


import Image

try:
    img = Image.open(imgname)
except IOError:
    exit("File not found: " + imgname)

# resize to: the max of the img is 100px

maxLen = max(img.size)

width, height = img.size

rate = MaxLen / maxLen

width = int(rate * width)  # cast to int

height = int(rate * height)

img = img.resize((width, height))

# convert to L model,  therefore: pix[x, y] will get an average number
# ranges from 0 to 255
img = img.convert('L')

# get pix
pix = img.load()

color = "MNHQ$OC?7>!:-;."

string = ""

for h in xrange(height):  # first go through the height,  otherwise will roate
    for w in xrange(width):
        string += color[int(pix[w, h] * 14 / 255)]
    string += "\n"

# wrappe with html

style = """
<html>
    <head>
        <style>
        .imgtxt{
            line-height:""" + str(int(height / level)) + """px;
        }
    </style>
    </head>
"""

html = style + "<body><pre class=\"imgtxt\">" + string + "</pre></body><html>"

print html
