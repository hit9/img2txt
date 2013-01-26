img2txt
=======

Image to Ascii Text. Dead simple, something useless.

Sample:

.. image:: https://github.com/hit9/img2txt/raw/master/sample/test.jpg

.. image:: https://github.com/hit9/img2txt/raw/master/sample/html.png

Install
-------

::

    git clone https://github.com/hit9/img2txt.git
    python setup.py install

Usage
-----

::

    Usage: img2txt <imgfile> [--size=<size>] [--level=<level>]

sample usage::

    img2txt me.jpg --size=100 --level=10  > me.html

the arguments::

    --size             max length of the result
    --level            height/levle will get the line-height(here, height means the height of result)

WhyHTML
-------

Because, the line-height in the css make an important sense to the result's quality.

License
-------

BSD,  short and sweet.
