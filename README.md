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

Updated 12.23.2017

Gyro Data not yet supported.  <br>
Depending on the headset, you may be able to view gyros in manual control. <br>
Epoc+ gyros will not currently be displayed. <br>
Note: Switching to Gyro-mode may cause EEG to stop displaying.  <br>
Refresh the browser if this occurs. <br>

Recordings work, however it has not been tested with importing <br>
to any application, and the headers may need some work. <br>

Todo: <br>
 Fix (All, Counter) buttons. <br>
 Add Gyros. <br>
 Add Game. <br>
 Add Epoc+ Settings change. <br>
 Fix CSV header data. <br>
 Add OpenVIBE support. <br>
 Add Generic TCP layer. <br>
 Fix Misc. visual bugs with scrolling. <br>
 
* Feel free to offer comments and suggests via Issues, for further <br>
information check our Discord server.  Submit new push requests,  <br>
if you have something to contribute. <br>
