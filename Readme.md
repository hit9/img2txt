img2txt
=======

Image to Ascii Text, can output to html or ansi terminal.

Example
-------

![](example/jiaozhu.jpg)

1. `img2txt.py jiaozhu.jpg > without-color.html` : [demo](http://hit9.github.io/img2txt/example/without-color.html)
2. `img2txt.py jiaozhu.jpg --color > with-color.html`: [demo](http://hit9.github.io/img2txt/example/with-color.html)
3. `img2txt.py jiaozhu.jpg --ansi`: [demo](http://hit9.github.io/img2txt/example/ansi-terminal.png)

Installation
------------

```bash
$ virtualenv venv
$ . venv/bin/activate
(venv)$ pip install git+git://github.com/hit9/img2txt.git@master
```

Usage
-----

```
Usage:
  img2txt.py <imgfile> [--maxLen=<n>] [--fontSize=<n>] [--color] [--ansi] [--bgcolor=<#RRGGBB>] [--antialias]
  img2txt.py (-h | --help)

Options:
  -h --help             show this screen.
  --ansi                output an ANSI rendering of the image
  --color               output a colored HTML rendering of the image.
  --antialias           causes any resizing of the image to use antialiasing
  --fontSize=<n>        sets font size (in pixels) when outputting HTML,
                        default: 7
  --maxLen=<n>          resize image so that larger of width or height matches
                        maxLen, default: 100px
  --bgcolor=<#RRGGBB>   if specified, is blended with transparent pixels to
                        produce the output. In ansi case, if no bgcolor set, a
                        fully transparent pixel is not drawn at all, partially
                        transparent pixels drawn as if opaque
```

License
-------

BSD.
