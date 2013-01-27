#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: img2txt.py <imgfile> [--maxLen=<maxLen>]

"""

from docopt import docopt

dct = docopt(__doc__)

imgname = dct['<imgfile>']

maxLen = dct['--maxLen']

try:
    maxLen = float(maxLen)
except:
    maxLen = 100.0   # default maxlen: 100px


import Image

try:
    img = Image.open(imgname)
except IOError:
    exit("File not found: " + imgname)

# resize to: the max of the img is maxLen

width, height = img.size

rate = maxLen / max(width, height)

width = int(rate * width)  # cast to int

height = int(rate * height)

img = img.resize((width, height))

# convert to L model,  therefore: pix[x, y] will get an average number
# ranges from 0 to 255
img = img.convert('L')

# get pixels
pixel = img.load()

color = "MNHQ$OC?7>!:-;. "

string = ""

for h in xrange(height):  # first go through the height,  otherwise will roate
    for w in xrange(width):
        string += color[int(pixel[w, h] * 15 / 255)]
    string += "\n"

# wrappe with html

style = """
<html>
    <head>
        <style>
        .imgtxt{
            line-height:""" + str(rate) + """;
        }
    </style>
    </head>
"""

html = style + "<body><pre class=\"imgtxt\">" + string + "</pre></body><html>"

print html
