from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.1'
DESCRIPTION = 'Collection iterator over classes'

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="pycollection",
    version=VERSION,
    author="Cristian Guzmán",
    author_email="<cristian.guzman.contacto@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["typing"],
    keywords=['python', 'collection', 'laravel', 'iterator', 'pycollection'],
    classifiers=[]
)