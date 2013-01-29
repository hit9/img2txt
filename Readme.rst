img2txt
=======

Image to Ascii Text. Dead simple, something useless.

**Online Demo**: http://hit9.org/img2txt.html

Sample:

.. image:: https://github.com/hit9/img2txt/raw/master/sample/test.jpg

.. image:: https://github.com/hit9/img2txt/raw/master/sample/html.png

Install
-------

::

    pip install git+git://github.com/hit9/img2txt.git

Usage
-----

::

    Usage: img2txt.py <imgfile> [--maxLen=<maxLen>] [--fontSize=<fontSize>] [--color]

sample usage::

    img2txt.py me.jpg --maxLen=100  --fontSize=3 --color > me.html

the optional arguments::

    --maxLen             max length of the result,default:100
    --color              if in color, default:False
    --fontSize           the font-size(px) of text in the html,default:7

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
