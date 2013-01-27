from setuptools import setup

setup(
    name="img2txt",
    version="0.1",
    author="hit9",
    author_email="nz2324@126.com",
    description=("Image to Ascii Text."),
    license="BSD", 
    url="https://github.com/hit9/img2txt",
    install_requires = ['docopt', 'PIL'],
    scripts=['img2txt.py']
)
