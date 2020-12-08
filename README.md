taskd-client-py
===============
[![PyPI version](https://img.shields.io/pypi/v/taskc.svg)](https://pypi.python.org/pypi/taskc)
[![Build Status](https://travis-ci.org/jrabbit/taskd-client-py.svg?branch=master)](https://travis-ci.org/jrabbit/taskd-client-py)

A client library providing an interface to [Taskd (from taskwarrior)](https://gothenburgbitfactory.org/projects/taskd.html)

Library users will have some obligations as per the protocol. (key storage, sync key, tasks themselves (and additional data), etc)


Getting Started
---------------
* `pip install taskc`
```python 
from taskc.simple import TaskdConnection
tc = TaskdConnection.from_taskrc() # only works if you have taskwarrior setup
resp = tc.pull()
```

User considerations
-------------------
* For taskd < 1.1.0 set `client.allow` in your taskd config ex: `client.allow=^task [2-9],^Mirakel [1-9],^taskc-py [0-9]`
* optionally enable connection debugging for output when running taskd interactively `debug.tls=2`
* for convience we're assuming ~/.task is your taskwarrior conf dir
* [if you run into trouble](https://taskwarrior.org/docs/taskserver/troubleshooting-sync.html)
