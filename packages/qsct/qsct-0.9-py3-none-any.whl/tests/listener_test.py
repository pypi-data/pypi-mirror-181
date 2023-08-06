from qsct import functions
from qsct.main import QSCT
import unittest
from socket import socket
import datetime


def Main_listener():
    host = "127.0.0.1"
    port = 5001

    mySocket = socket()
    mySocket.bind((host, port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    begin = datetime.datetime.now()
    listener = QSCT(True, "Слушатель")
    print("Connection from: " + str(addr))
    message = listener.get_obj(mySocket, conn)
    print(message)
    # while True:
    #     data = conn.recv(1024).decode()
    #     if not data:
    #         break
    #     print("from connected  user: " + str(data))
    #
    #     data = str(data).upper()
    #     print("Received from User: " + str(data))
    #
    #     data = input(" ? ")
    #     conn.send(data.encode())
    end1 = datetime.datetime.now() - begin
    end2 = end1 - datetime.timedelta(end1.seconds)
    print('Время выполнения: {}.{}'.format(end1.seconds, end2.microseconds))
    conn.close()

if __name__ == '__main__':
    Main_listener()