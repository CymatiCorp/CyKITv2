# -*- coding: utf8 -*-
#
# CyKIT v2 - 2017.12.23 
# ========================
# Emokit Written by Cody Brocious
# Emokit Written by Kyle Machulis
# CyKIT  Written by Warren
# Contributions  by Severin Lemaignan
# Contributions  by Sharif Olorin
# Contributions  by Bill Schumacher
# Contributions  by CaptainSmiley
#
import time
import os
import sys
import platform
import socket
import pywinusb.hid as hid
from Queue import Queue
from Crypto.Cipher import AES
from Crypto import Random
import threading
        
DEVICE_POLL_INTERVAL = 0.001  # in seconds

tasks = Queue()

class MyIO():
    
    def __init__(self):
        self.format = 0;
        self.newMask = None
        self.status = False
        self.setMask = []
        self.setMask = [None]*14
        self.recording = False
        self.recordInc = 1
        self.recordFile = "EEG_recording_"
        self.f = None
        
    def onData(self, uid, text):
        ioCommand = text.split(":::")
        if ioCommand[0] == "CyKITv2":
            if ioCommand[1] == "setModel":
                self.newModel = int(ioCommand[2])
                print "model=" + ioCommand[2]
            if ioCommand[1] == "changeFormat":
                self.format = int(ioCommand[2])
                if self.format == 1:
                    print "Format Change (Format-1): Javascript handling float conversion.\r\n"
                else:
                    print "Format Change (Format-0): Python handling float conversion.\r\n"
            if ioCommand[1] == "InfoRequest":
                self.server.sendData("CyKITv2:::Info:::Device:::" + str(self.infoDevice))
                self.server.sendData("CyKITv2:::Info:::Serial:::" + str(self.infoSerial))
            if ioCommand[1] == "RecordStart":
                if self.recording == True:
                    self.recording = False
                    try:
                        self.f.flush()
                        os.fsync(self.f.fileno())
                        self.f.close()
                    except:
                        pass
                    
                    print "[Record Stopped] -- Press 'Record' to Record a new file."
                    return
                    
                print "[Start] Recording to File: " + ioCommand[2]
                self.recordFile = str(ioCommand[2])
                
                pathFinder = './EEG-Logs/' + self.recordFile + '.csv'
                try:
                    while os.path.exists(pathFinder):
                        self.recordInc += 1
                        self.recordFile = self.recordFile + "-" + str(self.recordInc)
                        pathFinder = './EEG-Logs/' + self.recordFile + '.csv'
                        print "[Record: File exists. Changing to: " + self.recordFile + ".csv ]"
                except:
                    pass
                try:
                    self.f = file('./EEG-Logs/' + self.recordFile + '.csv', 'a')
                    self.f = open('./EEG-Logs/' + self.recordFile + '.csv', 'a')
                    cdate = datetime.datetime.now()
                    
                    
                    csvHeader = ""
                    csvHeader += "title: " + self.recordFile + ", "
                    csvHeader += "recorded: " + str(strftime("%d.%m.%y %H.%M.%S, "))
                    csvHeader += "timestamp started:2017-11-21T16:17:43.558438-08:00            , "
                    csvHeader += "sampling:" + self.samplingRate 
                    csvHeader += "subject:, "
                    csvHeader += "labels:COUNTER INTERPOLATED "
                    if self.KeyModel == 3 or self.KeyModel == 4:
                        # Insight
                        csvHeader += "AF3 T7 Pz T8 AF4 RAW_CQ GYROX GYROY MARKER SYNC TIME_STAMP_s TIME_STAMP_ms CQ_AF3 CQ_T7 CQ_Pz CQ_T8 CQ_AF4, "
                    else:
                        # Epoc/Epoc+
                        csvHeader += "AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4 "
                        csvHeader += "RAW_CQ GYROX GYROY MARKER MARKER_HARDWARE SYNC TIME_STAMP_s TIME_STAMP_ms "
                        csvHeader += "CQ_AF3 CQ_F7 CQ_F3 CQ_FC5 CQ_T7 CQ_P7 CQ_O1 CQ_O2 CQ_P8 CQ_T8 CQ_FC6 CQ_F4 CQ_F8 CQ_AF4 CQ_CMS CQ_DRL, "
                    csvHeader += "chan:40, "
                    csvHeader += "samples:5000, "
                    csvHeader += "units:emotiv\r\n"
                    print >>self.f, csvHeader
                    os.fsync(self.f.fileno())
                    self.recording = True
                    
                except:
                    pass
                
            if ioCommand[1] == "RecordStop":
                print "[Stop] Recording " 
                try:
                    self.f.flush()
                    os.fsync(self.f.fileno())
                    self.f.close()
                except:
                    pass
                self.recording = False
            if ioCommand[1] == "setMask":
                try:
                    maskSelect = int(ioCommand[2])
                    self.newMask = maskSelect
                    self.setMask[maskSelect] = map(int, str(ioCommand[3]).split("."))
                except Exception, msg:
                    print "Error: " + str(msg)
            #if ioCommand[1] == "ChangeSettings":
        #self.server.sendData("Incoming Data: %s"%(text,))
        return
    
    def onConnect(self, uid):
        self.status = True
        self.newMask = None
        self.server.sendData("CyKITv2:::Connected")
        return
        
    def sendData(self, uid, text):
        self.server.sendData(text)
        return      
        
    def status(self):
        return self.status
    
    def onClose(self, uid):
        self.running = False
        return
    
    def modelChange(self):
        if 'newModel' not in globals():
            return 0
        aModel = self.newModel
        self.newModel = 0
        return self.aModel
    
    def startRecord(self, recordPacket):
        try:
            print >>self.f, recordPacket
            self.f.flush()
            os.fsync(self.f.fileno())
        except:
            pass

    def stopRecord(self):
        try:                 
            self.f.flush()
            os.fsync(self.f.fileno())
            self.f.close()
        except:
            pass
            
    def formatChange(self, newFormat):
        self.format = newFormat
        return
        
    def formatStatus(self):
        return self.format
        
    def isRecording(self):
        return self.recording
        
    def maskChange(self):
        return self.newMask
    
    def getMask(self, select):
        self.newMask = None
        return self.setMask[int(select)]
    
    def setInfo(self, info, infoData):

        if info == "Device":
            self.infoDevice = str(infoData)
        if info == "Serial":
            self.infoSerial = str(infoData)
            
        return
        
    def setServer(self, server):
        self.server = server
        return
        
class EEG(object):
    
    def __init__(self, model, io, config):
        global running
        global myIOinstance
        config = config.lower()
        self.KeyModel = model
        self.eeg_devices = []
        self.running = True
        self.counter = "0"
        self.serial_number = ""
        self.lock = threading.Lock()
        self.hid = None
        self.myIOinstance = io
        self.myKey = self.Setup(model, config)
        self.recordInc = 1
        self.thread = threading.Thread(name='eegThread', target=self.run, kwargs={'key': self.myKey, 'myio': self.myIOinstance })
        self.thread.setDaemon = False
        self.stop_thread = False
        self.samplingRate = 128
        
        self.mask = {}
        self.mask[0] = [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7]
        self.mask[1] = [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9]
        self.mask[2] = [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27]
        self.mask[3] = [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45]
        self.mask[4] = [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63]
        self.mask[5] = [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65]
        self.mask[6] = [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83]
        self.mask[7] = [140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121]
        self.mask[8] = [158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139]
        self.mask[9] = [160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157]
        self.mask[10] = [178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175]
        self.mask[11] = [196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177]
        self.mask[12] = [214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195]
        self.mask[13] = [216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213]
        
        if "blankdata" in config:
            self.blank_data = True
        else:
            self.blank_data = False
        
        if "noCounter" in config:
            self.no_counter = True
        else:
            self.no_counter = False
            
        if "format" in config:
            myFormat = str(config).split("format-")
            self.format = int(myFormat[1][:1])
        else:
            self.format = 0
        
        if "nobattery" in config:
            self.nobattery = True
        else:
            self.nobattery = False
        
        if "outputdata" in config:
            self.outputData = True
        else:
            self.outputData = False
        
        if "outputencrypt" in config:
            self.outputEncrypt = True
        else:
            self.outputEncrypt = False
        
        print "Format: " + str(self.format)
        self.myIOinstance.formatChange(self.format)
        
    def start(self):
        for t in threading.enumerate():
            if 'eegThread' == t.getName():
                return
        self.running = True
        self.thread.start()
        return self.myIOinstance

    
    def Setup(self, model, config):
        # 'EPOC BCI', 'Brain Waves', 'Brain Computer Interface USB Receiver/Dongle', 'Receiver Dongle L01'
        deviceList = ['EEG Signals', '00000000000', 'Emotiv RAW DATA']
        devicesUsed = 0
        
        threadMax = 0
        for t in threading.enumerate():
            if t.getName()[:6] == "Thread": 
                threadMax += 1
                
        for device in hid.find_all_hid_devices():
            if "info" in config:
                print "Product name " + device.product_name
                print "device path " + device.device_path
                print "instance id " + device.instance_id
                print "_" * 80 + "\r\n"
            useDevice = ""
            for i, findDevice in enumerate(deviceList):
                
                if device.product_name == deviceList[i]:
                    print "\r\n>>> Found EEG Device >>> " +  findDevice + "\r\n"
                    if "confirm" in config:
                        useDevice = raw_input("Use this device? [Y]es? ")
                    else:
                        useDevice = "Y"
                    if useDevice.upper() == "Y":
                        devicesUsed += 1
                        self.hid = device
                        if threadMax < 2:
                            self.hid.open()
                        self.serial_number = device.serial_number
                        if threadMax < 2:
                            device.set_raw_data_handler(self.dataHandler)
                        print "> Using Device: " + device.product_name + "\r\n"
                        print "  Serial Number: " + device.serial_number + "\r\n\r\n"
        
        if devicesUsed == 0 or i == 0:
            print "\r\n> No Device Selected. Exiting . . ."
            os._exit(0)
        
        self.myIOinstance.setInfo("Device", device.product_name)
        self.myIOinstance.setInfo("Serial", device.serial_number)
            
        sn = self.serial_number
        
        k = ['\0'] * 16
        
        
        # --- Model 1 > [Epoc::Research]
        if model == 1:
            k = [sn[-1],'\0',sn[-2],'H',sn[-1],'\0',sn[-2],'T',sn[-3],'\x10',sn[-4],'B',sn[-3],'\0',sn[-4],'P']
            self.samplingRate = 128
            
        # --- Model 2 > [Epoc::Standard]
        if model == 2:   
            k = [sn[-1],'\0',sn[-2],'T',sn[-3],'\x10',sn[-4],'B',sn[-1],'\0',sn[-2],'H',sn[-3],'\0',sn[-4],'P']
            self.samplingRate = 128
            
        # --- Model 3 >  [Insight::Research]
        if model == 3:
            k = [sn[-2],'\0',sn[-1],'D',sn[-2],'\0',sn[-1],'\x0C',sn[-4],'\0',sn[-3],'\x15',sn[-4],'\0',sn[-3],'X']
            self.samplingRate = 128
            
        # --- Model 4 > [Insight::Standard]
        if model == 4: 
            k = [sn[-1],'\0',sn[-2],'\x15',sn[-3],'\0',sn[-4],'\x0C',sn[-3],'\0',sn[-2],'D',sn[-1],'\0',sn[-2],'X']
            self.samplingRate = 128
            
        # --- Model 5 > [Epoc+::Research]
        if model == 5:
            k = [sn[-2],sn[-1],sn[-2],sn[-1],sn[-3],sn[-4],sn[-3],sn[-4],sn[-4],sn[-3],sn[-4],sn[-3],sn[-1],sn[-2],sn[-1],sn[-2]]
            self.samplingRate = 256
            
        # --- Model 6 >  [Epoc+::Standard]
        if model == 6:
            k = [sn[-1],sn[-2],sn[-2],sn[-3],sn[-3],sn[-3],sn[-2],sn[-4],sn[-1],sn[-4],sn[-2],sn[-2],sn[-4],sn[-4],sn[-2],sn[-1]]
        
        key = ''.join(k)
        print "key = " + str(key)
        return str(key)
            

    def dataHandler(self, data):
        try:
            if self.blank_data == True:
                if data != "": return
                data = [0, 11, 45, 226, 13, 209, 11, 156, 77, 16, 118, 83, 208, 255, 75, 10, 40, 241, 206, 231, 146, 226, 59, 124, 165, 69, 24, 248, 163, 55, 25, 133, 167]
        
            if self.outputEncrypt == True:
                print str(data)
        except:
            pass
        tasks.put(''.join(map(chr, data[1:])))
        return True
  
    def convertEPOC(self, data, bits):
        level = 0
        for i in range(13, -1, -1):
            level <<= 1
            b, o = (bits[i] / 8) + 1, bits[i] % 8
            level |= (ord(data[b]) >> o) & 1
        return level
    
    def convertEPOC_PLUS(self, value_1, value_2):
        
        edk_value = "%.8f" % (((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) -128) * 32.82051289))
        #edk_value = "%.6f" % (((int(value_2) * .128205148) + 4201.02564096001) + ((int(value_1) -128) * 32.82051286))
        return edk_value
         
    def run(self, key, myio):
        
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_ECB, iv)
        
        self.lock.acquire()
        thread_name = ""
        print "\r\nActive Threads = {"
        for t in threading.enumerate():
            try:
                thread_name = str(t).split("(")
            except:
                continue
            
            print "   " + str(thread_name[0]) + " ::: " + str(t.getName()) + ">"
        print "} \r\n"
        self.lock.release()
                
        if self.myIOinstance.status == True:
            myio.sendData(1, "CyKITv2:::Info:::Device:::" + str(self.hid.product_name))
            myio.sendData(1, "CyKITv2:::Info:::Serial:::" + str(self.serial_number))
            myio.sendData(1, "CyKITv2:::Info:::KeyModel:::" + str(self.KeyModel))
            
        while self.running:
            if self.myIOinstance.status != True:
                return        
            if self.blank_data == True:
                self.dataHandler("")
              
            while not tasks.empty():
                check_mask = self.myIOinstance.maskChange()
                
                self.format = self.myIOinstance.formatStatus();
                
                if check_mask != None:
                    self.mask[check_mask] = self.myIOinstance.getMask(check_mask)
                    print self.mask[check_mask]
                task = tasks.get()
                
                try:
                    data = cipher.decrypt(task[:16]) + cipher.decrypt(task[16:])
                
                    counter_data = ""
                    packet_data = ""
                    
                    if self.KeyModel == 0:
                        counter_data = str(ord(data[0])) + " "
                        for i in range(1,len(data)):
                            packet_data = packet_data + str(ord(data[i])) + " "
                            
                    if self.KeyModel == 2:
                        counter_data = str(ord(data[0])) + " "

                        # No Format (Default)
                        if self.format < 1:
                            for i in range(0,14):
                                packet_data = packet_data + str(self.convertEPOC(data, self.mask[i])) + " "
                            if self.myIOinstance.isRecording() == True:
                                self.myIOinstance.startRecord(counter_data + packet_data)
                            if self.outputData == True:
                                print str(counter_data + packet_data)
                        
                        # Format 1
                        if self.format == 1:
                            for i in range(1, len(data)):
                                packet_data = packet_data + str(ord(data[i])) + " "
                            if self.myIOinstance.isRecording() == True:
                                self.myIOinstance.startRecord(counter_data + packet_data)
                            if self.outputData == True:
                                    print str(counter_data + packet_data)
                                        
                    if self.KeyModel == 4:
                        counter_data = str(ord(data[0])) + " "
                        if self.format < 1:
                            for i in range(0,14):
                                packet_data = packet_data + str(self.convertEPOC(data, self.mask[i])) + ".0 "
                            if self.myIOinstance.isRecording() == True:
                                self.myIOinstance.startRecord(counter_data + packet_data)
                            if self.outputData == True:
                                print str(counter_data + packet_data)
                        
                        if self.format == 1:
                            for i in range(1,len(data)):
                                packet_data = packet_data + str(ord(data[i])) + " "
                            if self.myIOinstance.isRecording() == True:
                                self.myIOinstance.startRecord(counter_data + packet_data)
                            if self.outputData == True:
                                print str(counter_data + packet_data)
                    
                    if self.KeyModel == 6:
                        
                        if self.no_counter == True:
                            counter_data = ""
                        else:
                            counter_data = str(ord(data[0])) + " " + str(ord(data[1])) + " "
                                
                        # Format 0: Default.  
                        if self.format < 1:
                            for i in range(2,16,2):
                                packet_data = packet_data + str(self.convertEPOC_PLUS(str(ord(data[i])), str(ord(data[i+1])))) + " "
                            
                            for i in range(18,len(data),2):
                                packet_data = packet_data + str(self.convertEPOC_PLUS(str(ord(data[i])), str(ord(data[i+1])))) + " "
                            
                            if self.nobattery == False:
                                    packet_data = packet_data + str(ord(data[16])) + " " + str(ord(data[17])) 
                            
                            if self.myIOinstance.isRecording() == True:
                                self.myIOinstance.startRecord(counter_data + packet_data)
                            
                            if self.outputData == True:
                                print str(counter_data + packet_data)
                                
                        # Format 1    
                        if self.format == 1:
                                for i in range(2,16,2):
                                    packet_data = packet_data + str(ord(data[i])) + " " + str(ord(data[i+1])) + " "

                                for i in range(18,len(data),2):
                                    packet_data = packet_data + str(ord(data[i])) + " " + str(ord(data[i+1])) + " "
                                
                                if self.myIOinstance.isRecording() == True:
                                    self.myIOinstance.startRecord(counter_data + packet_data)
                                
                                if self.nobattery == False:
                                    packet_data = packet_data + str(ord(data[16])) + " " + str(ord(data[17])) 
                                
                                if self.outputData == True:
                                    print str(counter_data + packet_data)
                        
                        #openvibe
                        #cy = struct.pack('>' + str(len(values)) + 'h',*values)
                        
                    try:
                        myio.sendData(1, counter_data + packet_data)

                    except Exception, msg:
                        if msg[0] == 9 or msg[0] == 10053 or msg[0] == 10035:
                            print "\r\nConnection Closing.\r\n"
                            self.running = False
                            tasks.queue.clear()
                            myio.onClose(1)
                            self.hid.close()
                            self.myIOinstance.stopRecord()
                            continue
                        print "eeg().run() sendData() Error: " + str(msg)

                except Exception, exception2:
                    print str(exception2)
