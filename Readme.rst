img2txt
-------

Image to Ascii Text. Dead simple, something useless.

Sample:

.. image:: https://github.com/hit9/img2txt/raw/master/sample/test.jpg

.. image:: https://github.com/hit9/img2txt/raw/master/sample/html.png

Install
-------

::

    [sudo] pip install git+git://github.com/hit9/img2txt.git

Usage
-----

::

    Usage: img2txt <imgfile> [--size=<size>] [--level=<level>]

sample usage::

    img2txt me.jpg --size=100 --level=10  > me.html

the arguments::

    --size             max length of output
    --level            size/levle will get the lineheight

WhyHTML
-------

Because, the line-height in the css make an important sense to the result's quality.

License
-------

BSD,  short and sweet.
