import serial
from ftplib import FTP
import time

ser = serial.Serial(2, 9600)
last_received = 0.0

def sendFile():
    ftp = FTP('hillbuntu')
    ftp.login('jared','fr33cycle')
    cur_temp_file = open('cur_temp.txt', 'rb')
    ftp.cwd('/var/www/jaredpavan.com/arduino/arduino_data')
    ftp.storbinary('STOR cur_temp.txt', cur_temp_file)
    cur_temp_file.close()
    ftp.quit()
    print 'File transfered'
    

def saveTemp(last_received):
    f = open('cur_temp.txt', 'w')
    f.write(str(last_received))
    f.close
    print 'File updated'

def receiving(ser):
    global last_received

    buffer = ''
    while True:
        buffer = buffer + ser.read(ser.inWaiting())
        if '\n' in buffer:
            lines = buffer.split('\n')
            last_received = lines[-2]
            buffer = lines[-1]
        print 'Temperature:', last_received
        saveTemp(last_received)
        sendFile()
        time.sleep(5)

receiving(ser)
