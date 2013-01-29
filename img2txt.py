#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: img2txt.py <imgfile> [--maxLen=<maxLen>] [--color]

"""

from docopt import docopt

dct = docopt(__doc__)

imgname = dct['<imgfile>']

maxLen = dct['--maxLen']

clr = dct['--color']

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

# img = img.convert('L')

# get pixels
pixel = img.load()

# grayscale
color = "MNHQ$OC?7>!:-;. "

string = ""

for h in xrange(height):  # first go through the height,  otherwise will roate
    for w in xrange(width):
        rgb = pixel[w, h]
        char = color[int(sum(rgb) / 3.0 / 256.0 * 16)]
        if clr:
            string += "<span style=\"color:rgb" + str(rgb) + \
                ";\">" + char + "</span>"
        else:
            string += char
    string += "\n"

# wrappe with html

style = """
<html>
    <head>
        <style>
        .imgtxt{
            font-size:7px;
            line-height:7px;
        }
    </style>
    </head>
"""

html = style + "<body><pre class=\"imgtxt\">" + string + "</pre></body><html>"

print html
