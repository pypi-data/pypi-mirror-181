import datetime
from socket import *
import threading
import pickle
import psycopg2


class Running:
    def __init__(self):
        self.run = True

    def get_run(self):
        return self.run

    def set_run(self, val):
        self.run = val


class ObjectStream:

    def __init__(self, sock):
        self.sock = sock
        self.writer = sock.makefile('wb')
        self.reader = sock.makefile('rb')

    # Objects are sent/received as a 4-byte big-endian integer of
    # the pickled object data length, followed by the pickled data.

    def get_obj(self):
        header = self.reader.read(4)
        if not header:
            return None
        length = int.from_bytes(header, 'big')
        return pickle.loads(self.reader.read(length))

    def put_obj(self, obj):
        data = pickle.dumps(obj)
        header = len(data).to_bytes(4, 'big')
        self.writer.write(header)
        self.writer.write(data)
        self.writer.flush()  # important!

    def close(self):
        if self.sock is not None:
            self.writer.close()
            self.reader.close()
            self.sock.close()
            self.sock = None
            self.writer = None
            self.reader = None

    # Support for 'with' to close everything.

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    # Support for no more references to ObjectStream

    def __del__(self):
        self.close()


class Sender:
    def __init__(self):
        self.run = Running()

    def server(self, sock, conn, *args, **kwargs):
        # s = socket()
        # s.bind(('', 9999))
        # s.listen(1)
        with sock:
            while self.run.get_run():
                # c, a = s.accept()
                # print('server: connect from', a)
                with ObjectStream(conn) as stream:
                    while True:
                        try:
                            obj = stream.get_obj()
                        except:
                            print("разорвано соединение")
                            obj = None
                        print('server:', obj)
                        if obj is None:
                            self.run.set_run(False)
                            # s.close()
                            # return obj
                            break
                        if isinstance(obj, list):
                            # reverse lists
                            # stream.put_obj(obj[::-1])
                            print(obj)
                            return obj
                        # elif isinstance(obj, dict):
                        #     # swap key/value in dictionaries
                        #     stream.put_obj({v: k for k, v in obj.items()})
                        #     print(obj)
                        #     return obj
                        else:
                            # otherwise, echo back same object
                            # stream.put_obj(obj)
                            print(obj)
                            return obj
                print("Передача закончена")
                # print('server: disconnect from', a)

    def client(self, sock, data, *args, **kwargs):
        # s = socket()
        # s.connect(('localhost', 9999))
        with ObjectStream(sock) as stream:
            begin = datetime.datetime.now()
            stream.put_obj(data)
            # print('client:', stream.get_obj())
            stream.put_obj({1: 2, 3: 4, 5: 6})
            # print('client:', stream.get_obj())
            stream.put_obj(None)
            end1 = datetime.datetime.now() - begin
            end2 = end1 - datetime.timedelta(end1.seconds)
            print('Время выполнения: {}.{}'.format(end1.seconds, end2.microseconds))


# running = Running()
# running.set_run(True)
# run = True  # Simple global flag to control server Thread
# threading.Thread(target=server).start()
# client()  # Server can handle only one client at a time as written.
# run = False
# running.set_run(False)
