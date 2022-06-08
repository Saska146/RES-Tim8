from http import client
import socket
import time
from struct import Struct
from threading import Thread
import threading
from enum import Enum
import random
from xml.dom import ValidationErr
import pickle

from cv2 import split

code = ["CODE_ANALOG", "CODE_DIGITAL", "CODE_CUSTOM", "CODE_LIMITSET", "CODE_SINGLENOE", "CODE_MULTIPLENODE", "CODE_CONSUMER", "CODE_SOURCE"]

class Item:
    def __init__(self, paket):
        self.paket = paket

    def __str__(self):
        return str(self.paket)
        
def KonekcijaKlijent():
    clientSocket = socket.socket()
    localHost = "127.0.0.1"
    port = 10254
    print("Cekanje na konekciju")
    try:
        clientSocket.connect((localHost, port))
        print("Konekcija na portu " + str(port) + " je uspjesna")
    except socket.error as e:
        print(str(e))

    return clientSocket

def SlanjePaketa():
    client = KonekcijaKlijent()
    while True:
        vrijednost = random.randint(0, 100)
        kod = random.choice(code)
        item = (str(kod)+ "?" +str(vrijednost))
        p = Item(item)
        client.send(str.encode(str(p)))
        print(item)
        time.sleep(2)

t1 = threading.Thread(target= SlanjePaketa)
t1.start()