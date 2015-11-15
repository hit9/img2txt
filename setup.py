from setuptools import setup

setup(
    name="img2txt.py",
    version="2.0",
    author="hit9",
    author_email="hit9@icloud.com",
    description="Image to Ascii Text, can output to html or ansi terminal.",
    license="BSD",
    url="http://hit9.org/img2txt",
    install_requires=['docopt', 'Pillow'],
    scripts=['img2txt.py']
)
