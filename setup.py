#! /usr/bin/env python

from setuptools import setup
from taskc import __version__
setup(name="taskc",
      version=__version__,
      packages=["taskc"],
      author="Jack Laxson",
      author_email="jackjrabbit@gmail.com",
      description="",
      license="GPL v3+",
      url="https://github.com/jrabbit/taskd-client-py",
      classifiers=["License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)", 
      "Development Status :: 2 - Pre-Alpha",
      "Intended Audience :: Developers",
                  ])
