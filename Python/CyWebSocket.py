# -*- coding: utf8 -*-
# 
# pywebsocketserver  2017.12.23
# ===============================
# Written  by suxianbaozi
#
# CyWebSocket.py     2017.12.23
# ===============================
# Modified by Warren
#
# Python web server for connecting sockets locally with browsers.
#

import sys
import socket
import time
import select
import threading
import hashlib
import base64
import struct

class socketIO():
    
    def __init__(self, port, uid, ioHandler):
        self.port = port
        self.con = None
        self.isHandleShake = False
        self.uid = uid
        self.io = ioHandler
        self.signKey = "ADS#@!D"
        self.online = True
        
        self.lock = threading.Lock()
        self.thread = threading.Thread(name='ioThread', target=self.run)
        self.thread.setDaemon = False

        self.stop_thread = False
        
    def start(self):
        self.socketThreadRunning = True
        #print "current thread === " + threading.currentThread().getName()
        #print "Thead alive?? " + str(self.Athread.is_alive)
        for t in threading.enumerate():
            print str(t.getName())
            if 'ioThread' == t.getName():
                return
        self.thread.start()
        

        
    def Handshake(self):
        
        self.isHandleShake = False
        self.online = True
        self.socketThreadRunning = True
        
    def Connect(self):
        
        print "* Connecting . . ."
        
        
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('',self.port))
        sock.listen(100)
        
        
        try:
            connection,address = sock.accept()
            self.con = connection
            print "> Connected!"
        except:
            print "> Not Connected -" + sock.error
        
        print str(self.con)
        
        
        return self.con
        
        #while 1:
        #    data = connection.recv(1024)
        #    if not data: break
            
        
    def run(self):       
        self.socketThreadRunning = True
        while self.socketThreadRunning == True:
        
            if not self.isHandleShake: 
                
                try:
                    self.con.setblocking(0)
                    ready = select.select([self.con], [], [], 1)
                    if ready[0]:
                        clientData  = self.con.recv(1024)
                        
                        #print clientData
                        dataList = clientData.split("\r\n")
                        header = {}
                        for data in dataList:
                            if ": " in data:
                                unit = data.split(": ")
                                header[unit[0]] = unit[1]
                        secKey = header['Sec-WebSocket-Key'];
                        resKey = base64.encodestring(hashlib.new("sha1",secKey+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest());
                        resKey = resKey.replace('\n','')
                        response = '''HTTP/1.1 101 Switching Protocols\r\n'''
                        response += '''Upgrade: websocket\r\n'''
                        response += '''Connection: Upgrade\r\n'''
                        response += '''Sec-WebSocket-Accept: %s\r\n\r\n'''%(resKey,)
                        self.con.send(response)
                        self.isHandleShake = True
                        
                        self.sendData("SETUID")
                        
                        self.io.onConnect(self.uid)
                        continue
                        
                except:
                    
                    continue
                    
            else:
                try:
                    
                    ready = select.select([self.con], [], [], 0)
                    
                    if ready[0]:
                        data_head = self.con.recv(1)
                        
                        if repr(data_head)=='':
                            #self.socketThreadRunning = False
                            self.onClose()
                            continue
                        
                        header = struct.unpack("B",data_head)[0]
                        opcode = header & 0b00001111
                        #print "Op Code %d"%(opcode,)

                        if opcode==8:
                            print "* Closing Connection."
                            self.socketThreadRunning = False
                            self.onClose()
                            
                            continue
                        
                        data_length = self.con.recv(1)
                        data_lengths= struct.unpack("B",data_length)
                        data_length = data_lengths[0]& 0b01111111
                        masking = data_lengths[0] >> 7
                        if data_length<=125:
                            payloadLength = data_length
                        elif data_length==126:
                            payloadLength = struct.unpack("H",self.con.recv(2))[0]
                        elif data_length==127:
                            payloadLength = struct.unpack("Q",self.con.recv(8))[0]
                        print "dataLen:%d"%(data_length,)
                        if masking==1:
                            maskingKey = self.con.recv(4)
                            self.maskingKey = maskingKey
                        data = self.con.recv(payloadLength)
                        if masking==1:
                            i = 0
                            true_data = ''
                            for d in data:
                                true_data += chr(ord(d) ^ ord(maskingKey[i%4]))
                                i += 1
                            self.onData(true_data)
                        else:
                            self.onData(data)
                    
                        
                except Exception, msg:
                    if msg[0] == 9 or msg[0] == 10053:
                        self.socketThreadRunning = False
                        
                    
                    print "CyWebSocket().socketIO() Error: " + str(msg)
                    
                    self.socketThreadRunning = False
                    self.onClose()
                    print str(msg[0])
                    return
            
            
    def onData(self,text) :
        print text
        try:
            uid,sign,value = text.split("<split>")
            uid = int(uid)
            print str(text)
        except:
            print "Error"
            self.con.close()
        hashStr = hashlib.new("md5",str(uid)+self.signKey).hexdigest()
        if hashStr!=sign:
            print "Hash Invalid"
            self.con.close()
            return
        return self.io.onData(uid,value)

    def onClose(self):
        self.con.close()
        self.online = False
        self.io.onClose(self.uid)

    def packData(self,text):
        sign = hashlib.new("md5",str(self.uid)+self.signKey).hexdigest()
        data = '%s<split>%s<split>%s'%(self.uid,sign,text)
        
        return data
        
    def sendData(self,text) :
        
        text = self.packData(text)
        
        self.con.send(struct.pack("!B",0x81))
        
        length = len(text)
       # masking = 0b00000000;

        if length<=125:
            self.con.send(struct.pack("!B",length))

        elif length<=65536:
            self.con.send(struct.pack("!B",126))
            self.con.send(struct.pack("!H",length))
        else:
            self.con.send(struct.pack("!B",127))
            self.con.send(struct.pack("!Q",length))

        self.con.send(struct.pack("!%ds"%(length,),text))
        
