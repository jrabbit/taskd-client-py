#! /usr/bin/env python

from setuptools import setup
from taskc import __version__
setup(name="taskc",
      version=__version__,
      packages=["taskc"],
      author="Jack Laxson",
      author_email="jackjrabbit@gmail.com",
      description="A python client library for taskwarrior's taskd",
      license="GPL v3+",
      url="https://github.com/jrabbit/taskd-client-py",
      classifiers=["License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                   "Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "Programming Language :: Python :: 2 :: Only",
                   "Programming Language :: Python :: 2.7",
                   ])
