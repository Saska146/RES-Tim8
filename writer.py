from http import client
import pickle
import random
import socket
import threading
import time

from models2 import *
from load_balancer import listaWorkera
from worker import *

client_socket=socket.socket()

def Connect_fun(local_host,portt):
    localHost = local_host
    port = portt
    print('\nWaiting for connection')
    while True:
        try:
            client_socket.connect((localHost, port))
            break
        except OSError:
            client_socket.close()
            raise OSError("Pogresna ip adresa")
        except OverflowError:
            client_socket.close()
            raise OverflowError("OVERFLOWERROR")



def SlanjePaketa():  # pragma: no cover
    Connect_fun('127.0.0.1',10254)
    while True:
        rand_value = random.randint(0, 100)
        rand_code = random.choice(list(code))
        data = pickle.dumps(Item(CodeEnum[rand_code], rand_value))
        client_socket.send(data)
        time.sleep(2)


def Kontrola():  # pragma: no cover
    while True:
        print("Za paljenje workera unesite 1, a za gašenje unesite 2")
        a = input()
        if a == "1" or a == "2":
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


if __name__ == '__main__':  # pragma: no cover
    t1 = threading.Thread(target=SlanjePaketa)
    t1.start()
    t2 = threading.Thread(target=Kontrola)
    t2.start()
