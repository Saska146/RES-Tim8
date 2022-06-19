import pickle
import random
import socket
import threading
import time
import logger
import models
from load_balancer import listaWorkera
from worker import *

localHost = "127.0.0.1"
port = 10254
global client_socket

def Connect():  # pragma: no cover
    global client_socket
    client_socket = socket.socket()
    print('Waiting for connection')
    while True:
        try:
            client_socket.connect((localHost, port))
            break
        except socket.error as e:
            print('.')

def KonekcijaKlijent():
    clientSocket = socket.socket()
    localHost = "127.0.0.1"
    port = 10254
    print("Cekanje na konekciju")
    while True:
        try:
            clientSocket.connect((localHost, port))
            print("Konekcija na portu " + str(port) + " je uspjesna")
            break
        except socket.error as e:
            print(str(e))

    return clientSocket

def SlanjePaketa():
    Connect()
    while True:
        rand_value = random.randint(0, 100)
        rand_code = random.choice(models.code)
        data = pickle.dumps(Item(CodeEnum[rand_code], rand_value))
        client_socket.send(data)
        time.sleep(2)

def Kontrola():
    while True:
        print("Za paljenje workera unesite 1, a za gašenje unesite 2")
        a = input()
        if (a == "1" or a == "2"):
            if a == "1":
                logger.logData("Paljenje novog workera.")
                noviWorker = Worker(len(listaWorkera) + 1)
                data = pickle.dumps(noviWorker)
                client_socket.send(data)
                listaWorkera.append(noviWorker)
                print("Lista: ")
                for r in listaWorkera:
                    print(r)
            elif a == "2":
                logger.logData("Gasenje workera.")
                data = pickle.dumps('REMOVE')
                client_socket.send(data)
                listaWorkera.pop()
                print("Lista: ")
                for r in listaWorkera:
                    print(r)
        else:
            print("Opcija sa datim brojem ne postoji, unesite ponovo")


if __name__ == '__main__':
    t1 = threading.Thread(target=SlanjePaketa)
    t1.start()
    t2 = threading.Thread(target=Kontrola)
    t2.start()
