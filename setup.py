from setuptools import setup

setup(
    name="img2txt.py",
    version="2.4",
    author="hit9",
    author_email="hit9@icloud.com",
    description="Image to Ascii Text, can output to html or ansi terminal.",
    license="BSD",
    url="https://github.com/hit9/img2txt",
    install_requires=['docopt', 'Pillow'],
    scripts=['img2txt.py'],
    py_modules=['ansi', 'graphics_util'],
)
