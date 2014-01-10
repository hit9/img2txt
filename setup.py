from setuptools import setup

setup(
    name="img2txt",
    version="1.1",
    author="hit9",
    author_email="nz2324@126.com",
    description=(
        """Image to Ascii Text with color support.Written in Python"""
    ),
    license="BSD",
    url="http://hit9.org/img2txt",
    install_requires = ['docopt', 'Pillow'],
    scripts=['img2txt.py']
)
