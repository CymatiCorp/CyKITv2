<img src="http://cymaticorp.com/edu/CyKITv2-/CyKITv2.png" width=25% height=25% ><br>
CyKit 2.0 (BETA) for Python 2.7.6 (Windows)

Python Data Controller for Neural EEG headsets.

Description
-----------
Streams EEG data to a browser for data handling.
Works with Chrome and Firefox.

<img src="http://cymaticorp.com/edu/CyKITv2-/CyKITv2-example.png" width=70% height=70% ><br>

Dependencies
------------
* pywinusb 0.4.2 --- https://pypi.python.org/pypi/pywinusb/  <br>
* pycrypto 2.6.1 --- https://pypi.python.org/pypi/pycrypto/2.6.1


Installation
------------
* Install Python 2.7.6
* Install pywinusb 

Usage
-----
example 1.
python.exe CyKITv2.py 127.0.0.1 18675 2

example 2.
python.exe CyKITv2.py 127.0.0.1 15309 4 info

example 3.
python.exe CyKITv2.py 127.0.0.1 12991 6 info+confirm


Open a browser. (Firefox/Chrome)

Enter port used to listen on, and press "Connect"

Features
--------

* Uses Python threading.
* Able to connect localy to localhost. (no need for http servers)
* Scrolling
* Able to make use of EEG data via javascript.
* EEG graphing.
* Masking (Advanced feature lets you manipulate data functions in real-time)

Beta
----
Currently the automatic rendering for certain EEG controllers does not work,
manual control should work for all devices.

Battery level might not report correctly on some devices.

Only the EEG tab is currently functional.

The data will not be formatted correctly on all controllers, and some additional
work needs to be done in this area.
