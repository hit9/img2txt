img2txt
=======

Image to Ascii Text, can output to html or ansi terminal.

HTML Demo
---------

The following picture: foo.jpg (230x354)

![](http://hit9.github.io/img2txt/foo.jpg)

1. `img2txt.py foo.jpg > 1.html` : [demo](http://hit9.github.io/img2txt/1.html)

1. `img2txt.py foo.jpg --color > 2.html` : [demo](http://hit9.github.io/img2txt/2.html)

1. `img2txt.py foo.jpg --color --fontSize=1 > 3.html`  : [demo](http://hit9.github.io/img2txt/3.html)

1. `img2txt.py foo.jpg --color --fontSize=1 --maxLen=354 > 4.html` : [demo](http://hit9.github.io/img2txt/4.html)

Installation
------------

```bash
$ virtualenv venv
$ . venv/bin/activate
(venv)$ pip install git+git://github.com/hit9/img2txt.git@master
```

Usage
-----

    Usage: img2txt.py <imgfile> [--maxLen=<n>] [--fontSize=<n>] [--color] [--ansi] [--bgcolor=<#RRGGBB>] [--antialias]

sample usage:

    img2txt.py me.jpg --maxLen=100  --fontSize=3 --color > me.html

the optional arguments:

    --ansi       output an ANSI rendering of the image
    --color      output a colored HTML rendering of the image.
    --antialias  causes any resizing of the image to use antialiasing
    --fontSize=<n>   sets font size (in pixels) when outputting HTML. Default is 7
    --bgcolor=<#RRGGBB>    if specified, is blended with transparent pixels to produce the output. In ansi case, if no bgcolor set, a fully transparent pixel is not drawn at all, partially transparent pixels drawn as if opaque
    --maxLen=<n>     resize image so that larger of width or height matches maxLen. Default is 100px

Warning
-------

Use browsers to look colored html may cause a big memory usage.

Hack!
-----

For instance , you have some pic: foo.jpg, and its size: axb, suppose a>b.

now, ``img2txt.py foo.jpg --maxLen=a --fontSize=1 --color > foo.html``

see foo.html in chrome or firefox, It looks like a picture!

WhyHTML
-------

Because it looks good in html.

License
-------

BSD,  short and sweet.
