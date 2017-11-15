# -*- coding: utf8 -*-
#
# CyKIT v2 - 2017.11
# ====================
# Emokit Written by Cody Brocious
# Emokit Written by Kyle Machulis
# CyKIT  Written by Warren
# Contributions  by Severin Lemaignan
# Contributions  by Sharif Olorin
# Contributions  by Bill Schumacher
#


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
        self.newMask = None
        self.status = False
        self.setMask = []
        self.setMask = [None]*14
    
    def onData(self, uid, text):
        print "incoming!" + text
        ioCommand = text.split(":::")
        if ioCommand[0] == "CyKITv2":
            if ioCommand[1] == "setModel":
                self.newModel = int(ioCommand[2])
                print "model=" + ioCommand[2]
            if ioCommand[1] == "InfoRequest":
                self.server.sendData("CyKITv2:::Info:::Device:::" + str(self.infoDevice))
                self.server.sendData("CyKITv2:::Info:::Serial:::" + str(self.infoSerial))
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
        print str(self.infoDevice)
        #self.status = False
        return
    
    def modelChange(self):
        if 'newModel' not in globals():
            return 0
        aModel = self.newModel
        self.newModel = 0
        return self.aModel
    
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
        
        self.KeyModel = model
        self.eeg_devices = []
        self.running = True
        self.counter = "0"
        self.serial_number = ""
        self.lock = threading.Lock()
        self.hid = None
        self.myIOinstance = io
        self.myKey = self.Setup(model, config)
            
        self.thread = threading.Thread(name='eegThread', target=self.run, kwargs={'key': self.myKey, 'myio': self.myIOinstance })
        self.thread.setDaemon = False
        self.stop_thread = False
    
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
    
    
    
    def start(self):
        self.running = True
        self.thread.start()
        return self.myIOinstance

    
    def Setup(self, model, config):
        # 'EPOC BCI', 'Brain Waves'
        deviceList = ['EEG Signals', '00000000000', 'Emotiv RAW DATA',"Brain Computer Interface USB Receiver/Dongle"]       
        devicesUsed = 0
        
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
                        self.hid.open()
                        self.serial_number = device.serial_number
                        device.set_raw_data_handler(self.dataHandler)
                        print "> Using Device: " + device.product_name + "\r\n"
                        print "  Serial Number: " + device.serial_number + "\r\n\r\n"
        
        if devicesUsed == 0 or i == 0:
            print "\r\n> No Device Selected. Exiting . . ."
            exit()
        
        self.myIOinstance.setInfo("Device", device.product_name)
        self.myIOinstance.setInfo("Serial", device.serial_number)
            
        sn = self.serial_number
        
        k = ['\0'] * 16
        
        
        # --- Model 1 > [Epoc::Research]
        if model == 1:
            k = [sn[-1],'\0',sn[-2],'H',sn[-1],'\0',sn[-2],'T',sn[-3],'\x10',sn[-4],'B',sn[-3],'\0',sn[-4],'P']
        
        # --- Model 2 > [Epoc::Standard]
        if model == 2:   
            k = [sn[-1],'\0',sn[-2],'T',sn[-3],'\x10',sn[-4],'B',sn[-1],'\0',sn[-2],'H',sn[-3],'\0',sn[-4],'P']
        
        # --- Model 3 >  [Insight::Research]
        if model == 3:
            k = [sn[-2],'\0',sn[-1],'D',sn[-2],'\0',sn[-1],'\x0C',sn[-4],'\0',sn[-3],'\x15',sn[-4],'\0',sn[-3],'X']
        
        # --- Model 4 > [Insight::Standard]
        if model == 4: 
            k = [sn[-1],'\0',sn[-2],'\x15',sn[-3],'\0',sn[-4],'\x0C',sn[-3],'\0',sn[-2],'D',sn[-1],'\0',sn[-2],'X']
        
        # --- Model 5 > [Epoc+::Research]
        if model == 5:
            k = [sn[-2],sn[-1],sn[-2],sn[-1],sn[-3],sn[-4],sn[-3],sn[-4],sn[-4],sn[-3],sn[-4],sn[-3],sn[-1],sn[-2],sn[-1],sn[-2]]
        
        # --- Model 6 >  [Epoc+::Standard]
        if model == 6:
            k = [sn[-1],sn[-2],sn[-2],sn[-3],sn[-3],sn[-3],sn[-2],sn[-4],sn[-1],sn[-4],sn[-2],sn[-2],sn[-4],sn[-4],sn[-2],sn[-1]]
        
        key = ''.join(k)
        return str(key)
            

    def dataHandler(self, data):
        tasks.put(''.join(map(chr, data[1:])))
        return True
  
    def get_level(self, data, bits):
        level = 0
        for i in range(13, -1, -1):
            level <<= 1
            b, o = (bits[i] / 8) + 1, bits[i] % 8
            level |= (ord(data[b]) >> o) & 1
        return level
        
    def new_level(self, data1, data2):
        mybits = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
        level = 0
        for i in range(13, -1, -1):
            level <<= 1
            b = (mybits[i] / 8) + 1
            o = (mybits[i] % 8)
            level |= (ord(data[b]) >> o) & 1
        return level

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
                continue
            while not tasks.empty():
                
                check_mask = self.myIOinstance.maskChange()
                
                if check_mask != None:
                    self.mask[check_mask] = self.myIOinstance.getMask(check_mask)
                    print self.mask[check_mask]
                task = tasks.get()

                try:
                    data = cipher.decrypt(task[:16]) + cipher.decrypt(task[16:])
                
                    apacket = ""
                    
                    if self.KeyModel == 0:
                        apacket = str(ord(data[0])) + " "
                        for i in range(0,len(data)):
                            apacket = apacket + str(data[i]) + " "
                            
                    if self.KeyModel == 2:
                        apacket = str(ord(data[0])) + " "
                        for i in range(0,14):
                            apacket = apacket + str(self.get_level(data, self.mask[i])) + " "
                    newdata = ''
                    
                    if self.KeyModel == 4 or self.KeyModel == 6:
                        apacket = str(ord(data[0])) + " " + str(ord(data[1])) + " "
                        
                        for i in range(2,len(data)):
                            apacket = apacket + str(ord(data[i])) + " "
                    
                    try:
                        myio.sendData(1, str(apacket))
                           
                    except Exception, msg:
                        if msg[0] == 9 or msg[0] == 10053 or msg[0] == 10035:
                            print "\r\nConnection Closing.\r\n"
                            self.running = False
                            tasks.queue.clear()
                            myio.onClose(1)
                            self.hid.close()
                            continue
                        print "eeg().run() sendData() Error: " + str(msg)
                    
                except Exception, exception2:
                    print str(exception2)
                
        
