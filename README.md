taskd-client-py
===============

A client library providing an interface to [Taskd (from taskwarrior)](http://tasktools.org/)

Library users will have some obligations as per the protocol. (key storage, sync key, tasks themselves (and additional data), etc)

User considerations
-------------------
* Set `client.allow` in your taskd config ex: `client.allow=^task [2-9],^Mirakel [1-9],^taskc-py [0-9]`
* optionally enable connection debugging for output when running taskd interactively `debug.tls=2`
* for convience we're assuming ~/.task is your taskwarrior conf dir

