#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: img2txt.py <imgfile> [--maxLen=<maxLen>] [--fontSize=<fontSize>] [--color]

"""

import sys

from docopt import docopt
from PIL import Image

dct = docopt(__doc__)

imgname = dct['<imgfile>']

maxLen = dct['--maxLen']

clr = dct['--color']

fontSize = dct['--fontSize']

try:
    maxLen = float(maxLen)
except:
    maxLen = 100.0   # default maxlen: 100px

try:
    fontSize = int(fontSize)
except:
    fontSize = 7



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
        if clr:
            string += "<span style=\"color:rgb" + str(rgb) + \
                ";\">▇</span>"
        else:
            string += color[int(sum(rgb) / 3.0 / 256.0 * 16)]
    string += "\n"

# wrappe with html

template = """<!DOCTYPE HTML>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <style type="text/css" media="all">
    pre {
      white-space: pre-wrap;       /* css-3 */
      white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
      white-space: -pre-wrap;      /* Opera 4-6 */
      white-space: -o-pre-wrap;    /* Opera 7 */
      word-wrap: break-word;       /* Internet Explorer 5.5+ */
      font-family: 'Inconsolata', 'Consolas'!important;
      line-height: 1.0;
      font-size: %dpx;
    }
  </style>
</head>
<body>
  <pre>%s</pre>
</body>
</html>
"""

html = template % (fontSize, string)
sys.stdout.write(html)
sys.stdout.flush()
