OpenViBE 2.0.0
================

Cykitv2 sends 14 channels of data. In either Integer or Float formats.
Connect to a localhost port above 1024 and below 32000<br>

* Start CyoKitv2.py with the following flags.
 `CyKITv2.py 127.0.0.1 5555 6 openvibe+generic+nocounter+nobattery+noheader+ovdelay:555+ovsamples:004+integer`

The `integer` flag sets the data to an integer. If you have an Epoc+ headset and your device is
capable of floating point data, do not include the `integer` flag.

* Install OpenViBE - http://openvibe.inria.fr/downloads/

* Start Acquisition Server.

* Start OpenViBE Designer.

[ Optional Step ]
If you require openvibe to read 1 sample at a time. Apply this patch.

* Open C:\Program files\OpenViBE\share\openvibe\applications\acquisition-server\interface.ui
```
Navigate to line 53 and edit the '4' digit, to a '1'
 like so:
       <col id="0" translatable="yes">1</col> 
```

Edit Acquisition Server preferences with the following parameters.

   * As `Driver` choose `Generic Raw Telnet Reader`.
   * Set the `Connection port` as `2222` and `Sample count per sent block` as `1`. - Connects to OpenViBE port.
   * In `Driver Properties`, set
     * `Number of channels`: `14`
     * `Sampling frequency`: `128` -- For Epoc+ try changing to 256 
     * `Telnet host name`: `localhost`
     * `Telnet host port`: `5555` - Connects to CyKit Port.
     * `Endianness`: `Big endian`
     * `Sample type`: `16 bits SIGNED integer` - (Requires 'integer' flag in CyKITv2.) 
     * `Skip at start (bytes)`: `0`
     * `Skip at header (bytes)`: `0`
     * `Skip at footer (bytes)`: `0`
     
`
Note: the "Sample type" can be either 16-bits SIGNED integer. or 32-bit float
CyKITv2 defaults to using a Float. so if you require your data to be an integer, make sure
to include the 'integer' flag.
`

* Click "Connect" on the OpenVIBE Acquisition server.

* Click `Play` (it should display `Sending...`)

1. Verify the Log will say "Connection succeeded!"
2. Verify Data is being read from the Python Cyos.py server.

<img src='http://cymaticorp.com/edu/openvibe/acquire5.png' width=100% height=100%></img>
Figure A.

1. Run "OpenVIBE Designer"
2. Drag and drop "Acquisition Client" from Boxes (on the right) to the white window space on the left.
3. Drag and drop "Signal display" as well.
4. Hover over the pink arrow. "Signal Stream [signal]" drag a line from that arrow<br>
   to the green arrow "Signal [streamed matrix]" until a line connects them.
5. Double click "Acquisition Client"
6. Replace server hostname with "localhost"
7. Replace server port with your designated OpenVIBE port. (ie. 2222)
8. Apply.


* Return to the "OpenVIBE acquisition server" and press "Play"

<img src='http://cymaticorp.com/edu/openvibe/acquire6.png' width=100% height=100%></img>
Figure B.

1. Return to the "OpenVIBE Designer" and press "Play"


1. A window will appear with your EEG stream.
2. Press Stop when completed or making signal changes.
