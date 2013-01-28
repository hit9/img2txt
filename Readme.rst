img2txt
=======

Image to Ascii Text. Dead simple, something useless.

Online Demo: http://hit9.org/img2txt.html

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

    Usage: img2txt.py <imgfile> [--maxLen=<maxLen>]

sample usage::

    img2txt.py me.jpg --maxLen=100  > me.html

the arguments::

    --maxLen             max length of the result,default:100

WhyHTML
-------

Because it looks good in html with a right line-height

License
-------

BSD,  short and sweet.
