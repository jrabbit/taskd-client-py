How to use taskc in your python app
===================================

..  highlight:: python

Here's a quickstart::

	from taskc.simple import TaskdConnection
	tc = TaskdConnection()
	# only works if you have taskwarrior setup
	tc = TaskdConnection.from_taskrc() 
	tc.connect()
	resp = tc.pull()

..