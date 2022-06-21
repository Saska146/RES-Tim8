import pickle
import random
import threading
from _thread import start_new_thread
from socket import socket

from Model.models import Description, Item
from worker import CodesForDataSet, Worker

listaWorkera = []
buffer = [Description(1, [], CodesForDataSet(1)), Description(2, [], CodesForDataSet(2)),
          Description(3, [], CodesForDataSet(3)), Description(4, [], CodesForDataSet(4))]
localHost = "127.0.0.1"
port = 10254


# TODO: Test
def startujServer(host, port):
    new_socket = socket()
    try:
        new_socket.bind((host, port))
    except:
        pass

    print(f'Server is listing on the port {port}...')
    new_socket.listen(1)
    return new_socket


def prihvatiKlienta(server_socket):  # pragma: no cover
    while True:
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=primiPoruke, args=(client_socket, client_address))
        thread.start()


def primiPoruke(client_socket, client_address):  # pragma: no cover
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


def sacuvajPodatke(item: Item):  # pragma: no cover
    for desc in buffer:
        if item.Code in desc.DataSet:
            desc.Items.append(item)
            print(f'saved {item}')


def zaposliWorkere():  # pragma: no cover
    while True:
        for desc in buffer:
            if len(desc.Items) > 0 and len(listaWorkera) > 0:
                worker = random.choice(listaWorkera)
                worker.ReceiveDescriptions(desc)
                print('Sent data to worker')


# TODO: Test
def nadjiWorkera():
    if len(listaWorkera) > 0:
        worker = random.choice(listaWorkera)
        return worker


if __name__ == '__main__':  # pragma: no cover
    serverSocket = startujServer(localHost, port)
    start_new_thread(prihvatiKlienta, (serverSocket,))
    zaposliWorkere()
