Updated Version (2017.12.23)

Chat Discussion:
https://discordapp.com/invite/gTYNWc7 <br>
(Do not need discord app, just click for browser chat)

<img src="./git-Images/CyKITv2.png" width=25% height=25% ><br>
CyKit 2.0 (2017.12) for Python 2.7.6 (Windows)

Python Data Controller for Neural EEG headsets.

Description
-----------
Streams EEG data to a browser for data handling.
Works with Chrome and Firefox.

<img src="./git-Images/CyKITpreview.png" width=70% height=70% ><br><br>
<img src="http://cymaticorp.com/edu/CyKITv2-/CyKITv2-example.png" width=70% height=70% ><br>

Dependencies
------------
* pywinusb 0.4.2 --- https://pypi.python.org/pypi/pywinusb/  <br>
* pycrypto 2.6.1 --- https://pypi.python.org/pypi/pycrypto/2.6.1


Installation
------------
* Install Python 2.7.6
* Install pycrypto
* Extract pywinusb-0.4.2
* Copy pywinusb/ folder to Python27\Lib\site-packages\

Usage
-----

<img src="./git-Images/helpFile.png" width=70% height=70% ><br>
example 1.
python.exe CyKITv2.py 127.0.0.1 18675 2

example 2.
python.exe CyKITv2.py 127.0.0.1 15309 4 info

example 3.
python.exe CyKITv2.py 127.0.0.1 12991 6 info+confirm


* Open a browser. (Firefox/Chrome)
* Open Web Document in project: /Web/CyKITv2.html
* Enter localhost and listen port used to run CyKITv2.py
* Press "Connect"

Features
--------

* Uses Python threading.
* Able to connect localy to localhost. (no need for http servers)
* Scrolling
* Able to make use of EEG data via javascript.
* EEG graphing.
* Masking (Advanced feature lets you manipulate data functions in real-time)

Note: Does not currently stream to openvibe. <br>
      Only a browser can access this data.

Beta
----
Currently the automatic rendering for certain EEG controllers does not work,
manual control should work for all devices.

Battery level might not report correctly on some devices.

Only the EEG tab is currently functional.

The data will not be formatted correctly on all controllers, and some additional
work needs to be done in this area.

* Feel free to offer comments and suggests via Issues, <br>
or submit new push requests, if you have something to contribute.
