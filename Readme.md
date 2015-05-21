img2txt
-------

Image to HTML ascii page converter.

Example
-----

Using the following picture: foo.jpg (230x354)

![](http://hit9.github.io/img2txt/foo.jpg)

1. `img2txt.py foo.jpg > 1.html` : [demo](http://hit9.github.io/img2txt/1.html)

2. `img2txt.py foo.jpg --color > 2.html` : [demo](http://hit9.github.io/img2txt/2.html)

3. `img2txt.py foo.jpg --color --fontSize=1 > 3.html`  : [demo](http://hit9.github.io/img2txt/3.html)

4. `img2txt.py foo.jpg --color --fontSize=1 --maxLen=354 > 4.html` : [demo](http://hit9.github.io/img2txt/4.html)

Installation
------------

```bash
$ virtualenv venv
$ . venv/bin/activate
(venv)$ pip install git+git://github.com/hit9/img2txt.git@master
```

Usage
-----

    Usage: img2txt.py <imgfile> [--maxLen=<maxLen>] [--fontSize=<fontSize>] [--color]

Example:

    img2txt.py image.jpg --maxLen=100 --fontSize=3 --color > me.html

Optional arguments:

    --maxLen             max length of the final generated image, default 100
    --color              have color output (HTML only), default False
    --fontSize           the font-size(px) of the html ascii art, default 7

Warning
-------

The generated color HTML may cause lag, due to its large file size.

License
-------

BSD
