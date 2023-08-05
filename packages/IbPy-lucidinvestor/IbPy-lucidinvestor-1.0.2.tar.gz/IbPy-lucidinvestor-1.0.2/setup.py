#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""IbPy - Interactive Brokers Python API

IbPy is a third-party implementation of the API used for accessing the
Interactive Brokers on-line trading system.  IbPy implements functionality
that the Python programmer can use to connect to IB, request stock ticker
data, submit orders for stocks and options, and more.
"""
import os.path
import codecs  # To use a consistent encoding
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Package name
pname = 'IbPy'
lucid_name = pname + '-lucidinvestor'

# Get the version ... execfile is only on Py2 ... use exec + compile + open
vname = 'version.py'
with open(os.path.join("ib", vname)) as f:
    exec(compile(f.read(), vname, 'exec'))

# Generate links
gurl = 'https://gitlab.com/algorithmic-trading-library/' + pname + "3"
gdurl = gurl + '/-/archive/' + __version__ + '/' + pname + "3" + '-' + __version__ + '.tar.gz'

try:  # Python 3
    from setuptools.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2
    from setuptools.command.build_py import build_py

setuptools.setup(
    cmdclass={'build_py': build_py},
    name=lucid_name,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    description='Interactive Brokers Python API (python 3 compatible version of https://github.com/blampe/IbPy) - '
                'maintained by LucidInvestor',
    long_description=long_description,

    # The project's main homepage.
    url=gurl,
    download_url=gdurl,

    # Author details
    author='maintainer: LucidInvestor - original: David Edwards (https://github.com/humdings) and Troy Melhase ('
           'troy@gci.net)',
    author_email='info@lucidinvestor.ca',

    # Choose your license
    license='BSD',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',

        # Indicate which Topics are covered by the package
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        ('License :: OSI Approved :: BSD License'),

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',

        # Operating Systems on which it runs
        'Operating System :: OS Independent',
    ],

    # What does your project relate to?
    keywords=['trading', 'development'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=setuptools.find_packages(),
    packages=['ib', 'ib/lib', 'ib/ext', 'ib/opt', 'ib/sym'],

    # List run-time dependencies here.
    # These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['six'],

)
