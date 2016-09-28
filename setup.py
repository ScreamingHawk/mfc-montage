from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mfcmontage',
    version='1.0.0',

    description='Generate images based on a users MyFigureCollection lists',
    long_description=long_description,

    url='https://github.com/ScreamingHawk/mfc-montage',

    author='Michael Standen',
    author_email='michael@standen.link',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        
        'Topic :: Games/Entertainment',

        'License :: OSI Approved :: MIT License',

        'Operating System :: Microsoft :: Windows',
        
        'Programming Language :: Python :: 3.5',
    ],

    keywords='image myfigurecollection montage',

    packages=['mfcmontage'],
)
