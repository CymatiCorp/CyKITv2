# -*- coding: utf8 -*-
#
# CyKIT v2 - 2017.12.23
# =======================
# Written by Warren
#

import sys
import socket
import select
import struct
import eeg
import CyWebSocket
import threading

arg_count = len(sys.argv)

if arg_count == 1 or arg_count > 5 or sys.argv[1] == "help" or sys.argv[1] == "--help" or sys.argv[1] == "/?":
    print "\r\n"
    print " (Version: CyKITv2:2017.12.15) -- Python 2.7.6 on Win32 \r\n"
    print "\r\n Usage:  Python.exe CyKITv2.py <IP> <Port> <Model#(1-6)> [config] \r\n"
    print " " + "_" * 85 + "\r\n"
    print " <IP> <PORT> for CyKIT to listen on. \r\n" 
    print " " + "_" * 85 + "\r\n"
    print " <Model#> Choose the decryption type. \r\n"
    print "          1 - Epoc (Research)\r\n"
    print "          2 - Epoc (Standard)\r\n"
    print "          3 - Insight (Research)\r\n"
    print "          4 - Insight (Standard)\r\n"
    print "          5 - Epoc+ (Research)\r\n"
    print "          6 - Epoc+ (Standard)\r\n\r\n"
    print " " + "_" * 85 + "\r\n"
    print " [config] is optional. \r\n"
    print "  'info' prints additional information into console.\r\n"
    print "  'confirm'  Requests you to confirm a device everytime device is initialized.\r\n"
    print "  'nocounter'  Removes all counters from 'all' outputs.\r\n"
    print "  'format-0' (Default) Outputs 14 data channels in float format. ('4201.02564096') \r\n"
    print "  'format-1' Outputs the raw data (to be converted by Javascript or other). \r\n"
    print "  'outputdata'  Prints the (formatted) data being sent, to the console window.\r\n"
    print "  'outputencrypt'  Prints the (encrypted) rjindael data to the console window.\r\n\r\n"
    print "   Join these words together, using a + separator. \r\n"
    print "   (e.g  info+confirm ) \r\n\r\n"
    print " " + "_" * 85 + "\r\n"
    print "  Example Usage: \r\n"
    print "  Python.exe CyKITv2.py 127.0.0.1 55555 1 info+confirm \r\n\r\n"
    print " " + "_" * 85 + "\r\n"
    sys.argv = [sys.argv[0], "127.0.0.1", "55555", "1", ""]
    
    
if arg_count < 5:
    
    if arg_count == 2:
        sys.argv = [sys.argv[0], sys.argv[1], "55555", "1", ""]
    if arg_count == 3:
        sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], "1", ""]
    if arg_count == 4:
        sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], ""]
   
        
"""
TODO
 
  Settings Buttons
   . Change Epoc+ settings mode.
  
  Send openvibe stream (using cyos template)
  
  Add Tabs
  
  Create CSS
   
  Associate checkboxes with drawing data.
  
"""

def main(CyINIT):

    if 'CyINIT' not in locals():
        #global CyINIT
        CyINIT = 2
   

    CyINIT += 1
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    MODEL = int(sys.argv[3])
    
    # Initialize CyKIT 
    if CyINIT == 2:
        global ioTHREAD
        print "> Listening on " + HOST + " : " + str(PORT)
        print "> Trying Key Model #: " + str(MODEL)
        
        myi = eeg.MyIO()
        ioTHREAD = CyWebSocket.socketIO(PORT, 1, myi)
        myi.setServer(ioTHREAD)
        check_connection = ioTHREAD.Connect()
        cyIO = ioTHREAD.start()
        cyHeadset = eeg.EEG(MODEL, myi, str(sys.argv[4])).start()
        for t in threading.enumerate():
            print str(t.getName())
        CyINIT += 1

    # Loop.
    
    while CyINIT > 2:
        CyINIT += 1
        
        if CyINIT > 100:
            modelCheck = myi.modelChange()
            if modelCheck != 0:
                MODEL = modelCheck
            
            CyINIT = 3
            check_threads = 0
            for t in threading.enumerate():
                if t.getName() == "ioThread" or t.getName() == "eegThread":
                    check_threads += 1
            
            if check_threads == 1:
                ioTHREAD.onClose()
                print "*** Reseting . . ."
                CyINIT = 1
                main(1)
            
        
        

    
try:
    
    main(1)
  
except Exception, e:
    print e
    print "Device Time Out or Disconnect . . .    Reconnect to Server."
    main(1)
