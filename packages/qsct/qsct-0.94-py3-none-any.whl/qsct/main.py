import pickle
import struct
import sys
import traceback
from qsct import functions
import hashlib
from _thread import allocate_lock


class QSCT:
    """QSCT - (Qodex Software Communication Tools) - это класс, представляющий из себя набор инструментов для
    создания API и SDK. Является супер-классом для суб-классов:
    1) QPI (Qodex Programming Interface) - API для ПО разработки компании Qodex,
    2) QDK (Qodex Development Kit) - SDK для взаимодействия с API ПО Qodex.
    QSCT опредлеяет методы передачи и получения данных, а также прочего взаимодействия между этими инструментами.
    """

    def __init__(self, debug=False, name=None, *args, **kwargs):
        """ Принимает атрибуты debug (вкл/выкл вывод в основной поток вывода информации о деятельности программы,
        name - собственное имя """
        self.status_ready = True
        self.debug = debug
        self.name = name
        self.send_locks = {}
        self.get_locks = {}

    def get_lock(self, sock, locks_dict):
        if sock in locks_dict:
            return locks_dict[sock]

    def create_lock(self, sock, locks_dict):
        locks_dict[sock] = allocate_lock()
        return locks_dict[sock]

    def lock_acquire(self, sock, locks_dict):
        lock = self.get_lock(sock, locks_dict)
        if not lock:
            lock = self.create_lock(sock, locks_dict)
        lock.acquire()
        return lock

    def lock_release(self, sock, locks_dict):
        lock = self.get_lock(sock, locks_dict)
        if not lock:
            lock = self.create_lock(sock, locks_dict)
        lock.release()
        return lock

    def send_data(self, sock, data, *args, **kwargs):
        """ Отправить сериализированные данные на WServer
        Протокол передачи такой - сначала длинна отправляемых данных, затем сами данные"""
        #self.mutex_send.acquire()
        self.show_print('\nОтправка данных:', data, debug=True)
        self.show_print('\tPickling...', debug=True)
        pickled_data = pickle.dumps(data)
        data_length = len(pickled_data)
        data_length_packed = struct.pack('>Q', data_length)
        self.show_print('\tОтправка длины...', data_length, debug=True)
        self.lock_acquire(sock, self.send_locks)
        try:
            sock.send(data_length_packed)
            self.show_print('\tОтправка данных...', debug=True)
            sock.send(pickled_data)
        except:
            print(traceback.format_exc())
            #self.lock_release(sock, self.send_locks)
        finally:
            print('БЛОК НА ОТПРАВКУ СНЯТ')
            self.lock_release(sock, self.send_locks)
        self.show_print('\tДанные были отправлены.', debug=True)

    def get_response(self, sock, *args, **kwargs):
        """Получить, показать и вернуть ответ"""
        response = self.get_data(sock)
        self.show_print('\tПолучен ответ', response, debug=True)
        return response

    def get_data(self, sock, *args, **kwargs):
        """Получить данные из сокета. Принимает данные в формате pickle, причем, сначала принимает длину данных,
        а потом сами данные """
        self.show_print('\nОжидаем данные', debug=True)
        packet = sock.recv(8)
        print("БЛОК НА ПОЛУЧЕНИЕ")
        if not packet:
            return
        self.lock_acquire(sock, self.get_locks)
        self.show_print('Got data: {}'.format(packet), debug=True)
        (data_length_unpacked,) = struct.unpack('>Q', packet)
        self.show_print('data length', data_length_unpacked, debug=True)
        data = b''
        try:
            while len(data) < data_length_unpacked:
                to_read = data_length_unpacked - len(data)
                data += sock.recv(4096 if to_read >= 4096 else to_read)
        except:
            return
        finally:
            print("БЛОК НА ПОЛУЧЕНИЕ СНЯТ")
            self.lock_release(sock, self.get_locks)
        try:
            unpickled_data = pickle.loads(data)
            return unpickled_data
        except:
            self.lock_release(sock, self.get_locks)



    def show_print(self, *msg, debug=False):
        """ Замена обычному print(), дополнительно получает аргумент debug, и если он положительный - информация msg
        будет выводиться в стандартный поток вывода, только если сам класс вызван с атрибутом debug"""
        msg = functions.make_str_tuple(msg)
        if debug and self.debug:
            print(msg)
        elif not debug:
            print(msg)

    def get_password_hash(self, password):
        return functions.get_password_hash(password)
