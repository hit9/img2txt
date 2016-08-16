img2txt
=======

Image to Ascii Text, can output to html or ansi terminal.

See also [gif2txt](https://github.com/hit9/gif2txt) for animated version.

Example
-------

![](example/jiaozhu.jpg)

1. `img2txt.py jiaozhu.jpg > without-color.html` : [demo](http://hit9.github.io/img2txt/example/without-color.html)
2. `img2txt.py jiaozhu.jpg --dither > without-color-dither.html` : [demo](http://hit9.github.io/img2txt/example/without-color-dither.html)
3. `img2txt.py jiaozhu.jpg --color > with-color.html`: [demo](http://hit9.github.io/img2txt/example/with-color.html)
4. `img2txt.py jiaozhu.jpg --ansi`: [demo](http://hit9.github.io/img2txt/example/ansi-terminal.png)

Installation
------------

```bash
$ virtualenv venv
$ . venv/bin/activate
(venv)$ pip install img2txt.py
```

Usage
-----

```
Usage:
  img2txt.py <imgfile> [--maxLen=<n>] [--fontSize=<n>] [--color] [--ansi] [--bgcolor=<#RRGGBB>] [--targetAspect=<n>] [--antialias] [--dither]
  img2txt.py (-h | --help)

Options:
  -h --help             show this screen.
  --ansi                output an ANSI rendering of the image
  --color               output a colored HTML rendering of the image.
  --antialias           causes any resizing of the image to use antialiasing
  --dither              dither the colors to web palette. Useful when converting
                        images to ANSI (which has a limited color palette)
  --fontSize=<n>        sets font size (in pixels) when outputting HTML,
                        default: 7
  --maxLen=<n>          resize image so that larger of width or height matches
                        maxLen, default: 100px
  --bgcolor=<#RRGGBB>   if specified, is blended with transparent pixels to
                        produce the output. In ansi case, if no bgcolor set, a
                        fully transparent pixel is not drawn at all, partially
                        transparent pixels drawn as if opaque
  --targetAspect=<n>    resize image to this ratio of width to height. Default is
                        1.0 (no resize). For a typical terminal where height of a
                        character is 2x its width, you might want to try 0.5 here
```

Authors
-------

- @EdRowe (#4, #7)
- @shakib609 (#10)
- @mattaudesse (#11)
- @hit9

License
-------

BSD.
