<img src="https://github.com/CymatiCorp/CyKITv2/blob/gitImages/git-Images/CyKITv2.png" width=25% height=25% ><br>
Updated Version (2018.Feb.06) 2:32pm


Chat Discussion:
https://discordapp.com/invite/gTYNWc7 <br>
(Do not need discord app, just click for browser chat)

CyKit 2.0 for Python 2.7.6 (32-bit) (Windows) <br>
Python Data Controller for Neural EEG headsets.

Description
-----------
Streams EEG data to a browser for data handling.
Works with Chrome and Firefox.

<img src="https://github.com/CymatiCorp/CyKITv2/blob/gitImages/git-Images/CyKITpreview.png" width=70% height=70% ><br><br>

Requirements
------------
* Windows
* Python 2.7.6
* 32-bit version of Python

```
pycrypto 2.6.1 (32-bit) and pywinusb 0.4.1 are now included into this repository.
(No installation necessary. Simply extract this repository to a folder and run.
see below for usage details.)
```

Usage
-----

<img src="https://github.com/CymatiCorp/CyKITv2/blob/gitImages/git-Images/helpFile.png" width=70% height=70% ><br>

```
example 1.
python.exe CyKITv2.py 127.0.0.1 18675 2

example 2.
python.exe CyKITv2.py 127.0.0.1 15309 4 info

example 3.
python.exe CyKITv2.py 127.0.0.1 12991 6 info+confirm
```

* Open a browser. (Firefox/Chrome)
* Open Web Document in project: /Web/CyKITv2.html
* Enter localhost and listen port used to run CyKITv2.py
* Press "Connect"

Optional Flags
--------------
<img src="https://github.com/CymatiCorp/CyKITv2/blob/gitImages/git-Images/help1.png" width=40% height=40% ><br>
'confirm' flag enabled, lets you manually confirm what device to use.

<img src="https://github.com/CymatiCorp/CyKITv2/blob/gitImages/git-Images/help2.png" width=70% height=70% ><br>
'info' flag enabled. View additional product information about your
usb devices.

<img src="https://github.com/CymatiCorp/CyKITv2/blob/gitImages/git-Images/help4.png" width=70% height=70% ><br>
'nocounter' flag enabled. The first 2 bytes (and delimiters) are not included<br>
in the output data. May be useful for formatting data for other applications.

Features
--------

* Uses Python threading.
* Able to connect locally to localhost. (no need for http servers)
* Scrolling
* Able to make use of EEG data via javascript.
* EEG graphing.
* Masking (Advanced feature lets you manipulate data functions in real-time)
* Streams to any program via TCP stream.
* EEG logging. Can display in Emotiv programs.

Note: Does not currently stream to openvibe. <br>


Bluetooth Support
-----------------
<img src="https://github.com/CymatiCorp/CyKITv2/blob/gitImages/git-Images/btle_win.png" width=80% height=80% ><br>

Currently CyKIT does not have bluetooth support integrated into it. However we can direct you to the
resources that incorporate bluetooth for Emotiv. Because Emotiv devices uses Bluetooth LE, which is not
natively supported in Windows 7 or below. It can only be run on Windows 8 or 10, which supports BTLE. 
Special Thanks to CaptainSmiley for creating this Bluetooth port:

![Bluetooth Development](https://github.com/CymatiCorp/CyKITv2/blob/gitImages/Documentation/Bluetooth_Development-Epoc.pdf) <br>
![Bluetooth Application](https://github.com/CymatiCorp/CyKITv2/blob/gitImages/Bluetooth/emotivBT.zip) <br>

OpenViBE Support
----------------
![OpenViBE Setup](https://github.com/CymatiCorp/CyKITv2/blob/gitImages/Documentation/OpenViBE.md)

Beta
----

Gyro Data --- Coming Soon.  <br><br>
Note: Switching to Gyro-mode may cause EEG to stop displaying.  <br>
Refresh the browser if this occurs. <br>

* Feel free to offer comments and suggests via Issues, for further <br>
information check our Discord server.  Submit new push requests,  <br>
if you have something to contribute. <br>
