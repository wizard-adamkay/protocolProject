import socket, pickle
import sys
from _thread import *
from packet import Packet
import time

myHost = 'localhost'
transmitterPort = 8000

nextAck = None

def listenToTransmitter():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))
    try:
        s.bind((myHost, transmitterPort))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    print('Socket bind complete')
    print("listening")
    s.listen(1)
    while True:  # listen until process killed
        connection, address = s.accept()
        print('Client Connection:', address)  # Print the connected client address
        start_new_thread(sendToTransmitter, ())
        while True:
            data = connection.recv(1024)  # read the client message
            data_variable = pickle.loads(data)
            print(data_variable.seqNum)
            global nextAck
            nextAck = Packet(1,1,b'',1,data_variable.seqNum+1)
            if data_variable.packetType == 2:
                break
        connection.close()
    s.close()

def sendToTransmitter():
    global nextAck
    HOST = 'localhost'
    PORT = 8001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while 1:
        if nextAck != None:
            packet = pickle.dumps(nextAck)
            s.send(packet)
            nextAck = None
        time.sleep(1)
    s.close()


start_new_thread(listenToTransmitter, ())

while 1:
    time.sleep(1)
