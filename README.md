# motion_python_api
Python wrapper for the Motion HTML API
Motion is a software motion detector used for turning linux systems into surveillance cameras. 
It is hosted at http://www.lavrsen.dk/foswiki/bin/view/Motion/WebHome
These are wrappers for the MotionHttpApi documented at http://www.lavrsen.dk/foswiki/bin/view/Motion/MotionHttpAPI

Sample usage:
from motion_detector_api import take_snapshot
take_snapshot(username="user", password="pass", port="8080")

Defaults to no username, no password, localhost:8080

Documentation will improve dramatically when I have the time

~~~
TODO:
Better documentation
Tests
Implement tracking wrappers
