# -*- coding: utf8 -*-
#
# CyKIT v2 - 2018.Jan.29
# ========================
# Written by Warren
#

import sys
import socket
import select
import struct
import eeg
import CyWebSocket
import threading
import time

arg_count = len(sys.argv)

if arg_count == 1 or arg_count > 5 or sys.argv[1] == "help" or sys.argv[1] == "--help" or sys.argv[1] == "/?":
    print "\r\n"
    print " (Version: CyKITv2:2018.Jan.29) -- Python 2.7.6 on Win32 \r\n"
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
    print "  'info'          Prints additional information into console.\r\n"
    print "  'confirm'       Requests you to confirm a device everytime device is initialized.\r\n"
    print "  'nocounter'     Removes all counters from 'all' outputs.\r\n"
    print "  'noheader'      Removes CyKITv2::: header information. (Required for openvibe) \r\n"
    print "  'format-0'      (Default) Outputs 14 data channels in float format. ('4201.02564096') \r\n"
    print "  'format-1'      Outputs the raw data (to be converted by Javascript or other). \r\n"
    print "  'outputdata'    Prints the (formatted) data being sent, to the console window.\r\n"
    print "  'outputencrypt' Prints the (encrypted) rjindael data to the console window.\r\n\r\n"
    print "  'blankdata'     Injects a single line of encrypted data into the stream that is \r\n"
    print "                   consistent with a blank EEG signal. Counter will report 0. \r\n\r\n"
    print "  'blancsv'       Adds blank channels for each CSV line, to be used with logging.\r\n\r\n"
    print "  'generic'       Connects to any generic program via TCP. (Can be used with other flags.)\r\n\r\n"
    print "  'openvibe'      Connects to the generic OpenViBE Acquisition Server.\r\n\r\n"
    print "                  must use generic+nocounter+noheader+nobattery Other flags are optional.\r\n"
    print "  'ovdelay'       Stream sending delay. (999 maximum) Works as a multiplier, in the format: ovdelay:001 \r\n\r\n"
    print "  'ovsamples'     Changes openvibe sample rate. Format: ovsamples:001 \r\n\r\n"
    print "  'integer'       Changes format from float to integer. Works with other flags. Including openvibe. \r\n\r\n"
    print "   Join these words together, using a + separator. \r\n"
    print "   (e.g  info+confirm ) \r\n\r\n"
    print " " + "_" * 85 + "\r\n"
    print "  Example Usage: \r\n"
    print "  Python.exe CyKITv2.py 127.0.0.1 55555 1 info+confirm \r\n\r\n"    
    print "  Example Usage: \r\n"
    print "  Python.exe CyKITv2.py 127.0.0.1 55555 6 openvibe+generic+nocounter++noheader+nobattery+ovdelay:100+integer+ovsamples:004 \r\n\r\n"
    print " " + "_" * 85 + "\r\n"
    sys.argv = [sys.argv[0], "127.0.0.1", "55555", "1", ""]
    
    
if arg_count < 5:
    
    if arg_count == 2:
        sys.argv = [sys.argv[0], sys.argv[1], "55555", "1", ""]
    if arg_count == 3:
        sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], "1", ""]
    if arg_count == 4:
        sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], ""]
   
    
   
def main(CyINIT):

    parameters = str(sys.argv[4]).lower()
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
        
        if "noheader" in parameters:
            myi.setHeader(True)
        if "openvibe" in parameters:
            myi.setOpenvibe(True)
        if "generic" in parameters:
            ioTHREAD = CyWebSocket.socketIO(PORT, 0, myi)
        else:
            ioTHREAD = CyWebSocket.socketIO(PORT, 1, myi)
        myi.setServer(ioTHREAD)
        check_connection = ioTHREAD.Connect()
        cyIO = ioTHREAD.start()
        
        cyHeadset = eeg.EEG(MODEL, myi, parameters).start()
        for t in threading.enumerate():
            print str(t.getName())
        CyINIT += 1
        if myi.getOpenvibe() == True:
            time.sleep(3)
        
    while CyINIT > 2:
        CyINIT += 1
        
        if CyINIT > 1000:
            modelCheck = myi.modelChange()
            if modelCheck != 0:
                MODEL = modelCheck
            
            CyINIT = 3
            check_threads = 0
            #print "testing"
            
            for t in threading.enumerate():
                if t.getName() == "ioThread" or t.getName() == "eegThread":
                    check_threads += 1
            
            if myi.getOpenvibe() == True:
                if check_threads == 0:
                    ioTHREAD.onClose()
                    print "*** Reseting . . ."
                    CyINIT = 1
                    main(1)
                continue
                
            
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
