import cv2
import time
import picamera
import socket
import io
import struct
import thread
import fcntl

IsGoVideo = 0


def get_local_ip(ifname = 'wlan0'):  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
    ret = socket.inet_ntoa(inet[20:24])  
    return ret  
  
def sendPic(sc,camera):
    camera.resolution = (800,600)
    mstream = io.BytesIO()
    camera.capture(mstream,'jpeg')
    buffer = mstream.getvalue()
    blen = len(buffer)
    comstr = struct.pack('cL','p',blen)
    print comstr[0]
    conn.send(comstr)
    conn.send(buffer)

def sendVideo(sc,camera):
    camera.resolution = (320,240)
    mstream = io.BytesIO()
    IsGoVideo = 1
    while IsGoVideo:
        msm1 = io.BytesIO()
        camera.capture(msm1,'jpeg')
        buffer=msm1.getvalue()
        blen = len(buffer)
        comstr = struct.pack('cL','v',blen)
        conn.send(comstr)
        conn.send(buffer)
    

camera = picamera.PiCamera()
camera.vflip = True
camera.hflip = True
HOST = get_local_ip()
print HOST
PORT = 2408
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)

while 1:
    conn,addr=s.accept()
    print 'client ip:',addr
    
    data=conn.recv(1024)
    print data
    if data=='get pic':
        thread.start_new_thread(sendPic,(conn,camera))
    elif data=='get video':
        thread.start_new_thread(sendVideo,(conn,camera))
    else:
        IsGoVideo = 0
        str=struct.pack('ci','x',0)
        conn.send(str)
    
s.close()
        
