import pickle
import random
from _thread import start_new_thread
from socket import socket

from models import *
from worker import CodesForDataSet, Worker

listaWorkera = []
buffer = [Description(1, [], CodesForDataSet(1)), Description(2, [], CodesForDataSet(2)),
          Description(3, [], CodesForDataSet(3)), Description(4, [], CodesForDataSet(4))]
localHost = "127.0.0.1"
port = 10254


def startujServer(host, port):
    new_socket = socket()
    try:
        new_socket.bind((host, port))
    except:
        pass

    print(f'Server is listing on the port {port}...')
    new_socket.listen(1)
    return new_socket


def prihvatiKlienta(server_socket):
    client_socket, client_address = server_socket.accept()
    primiPoruke(client_socket, client_address)


def primiPoruke(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(2048)
            message = pickle.loads(message)
            if isinstance(message, Worker):
                listaWorkera.append(message)
            elif message == 'REMOVE':
                listaWorkera.pop()
            else:
                sacuvajPodatke(message)
            print(f'Primio poruku od {client_address}:\t{message}')
        except:
            pass


def sacuvajPodatke(item: Item):
    for desc in buffer:
        if item.Code in desc.DataSet:
            desc.Items.append(item)
            print(f'saved {item}')


def zaposliWorkere():
    while True:
        for desc in buffer:
            if len(desc.Items) > 0 and len(listaWorkera) > 0:
                worker = random.choice(listaWorkera)
                worker.ReceiveDescriptions(desc)
                print('Sent data to worker')


if __name__ == '__main__':
    serverSocket = startujServer(localHost, port)
    start_new_thread(prihvatiKlienta, (serverSocket,))
    zaposliWorkere()
