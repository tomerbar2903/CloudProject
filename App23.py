"""
A program for executing cloud files
"""
import socket
import os
import sys
import time
import subprocess
import shutil
import psutil
from ReadRegistry import *

COMMANDS = ["UPLOAD_FILE", "UPLOAD_DIR", "DOWNLOAD_FILE"]
START = 0
END = -1
MSG_LEN = 1024
BYTE_NUMBER = 1024
FILE_DOESNT_EXIST = "file doesn't exist"
FILE_END = b'NO_MORE'
FILE_SENT = 'file uploaded successfully !!!'
MSG_FILL = 4
NO_PARAMETERS = 0
ONE_PARAMETER = 1
TWO_PARAMETER = 2
THREE_PARAMETERS = 3
BYTE = 4
PRM = 1
PORT = 6969
BIG_NUMBER = 1000
SERVER_FELL = str(1)
CLOUD_FORMAT = 'cloud'
CLOUD_REG = "CLIENT_CLOUD"
TEMPORARY_FILES = r"E:\12\Project\Temp"
START_COUNT = 1
SECOND = 1
CLOUD = r"E:\Check"
FILE_DOWNLOADED = 'file is opening right now...'
ON_CLOSE_APP = r"E:\12\Project\Classes\OpenFile.py"
PYTHON_LOCATION = r"C:\Program Files (x86)\Python37-32\python.exe"
IP = '127.0.0.1'
CLIENT_REG = r"SOFTWARE\Cloud Server\Client"
SERVER_REG = r"SOFTWARE\Cloud Server"
SHORT_SLEEP = 0.5
LONG_SLEEP = 3
VALUE_COUNT = 3
USERNAME_REG = "username"
REGISTRY_ZERO = 0


class Application(object):
    def __init__(self):
        """
        :param request: the request of the file to receive from server
        """
        # initiates request (clicked file path)
        self.request = Application.get_request()
        self.client_reg = ReadRegistry(CLIENT_REG)
        self.server_key = OpenKey(HKEY_LOCAL_MACHINE,
                                  SERVER_REG, REGISTRY_ZERO, KEY_READ)
        self.client_key = OpenKey(HKEY_LOCAL_MACHINE,
                                  CLIENT_REG, REGISTRY_ZERO, KEY_READ)

        ip, port = self.get_ip_port()
        self.ip = ip
        self.port = port
        self.cloud = Application.read_registry(HKEY_LOCAL_MACHINE,
                                               CLIENT_REG, CLOUD_REG)
        self.temp = self.cloud + APPINFO
        self.username = Application.read_registry(HKEY_LOCAL_MACHINE,
                                                  CLIENT_REG, USERNAME_REG)

        # initiates socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
            # sends the request to the server
            path_to_send = self.without_cloud(self.request)
            Application.send_request_to_server(self.sock,
                                               self.username +
                                               SEPERATOR + DOWNLOAD_FILE + SEPERATOR +
                                               path_to_send)
            format = Application.read_server_response(self.sock).decode()
            if format != ERROR_FORMAT:
                self.path_file = self.download(format)
                self.start_file_and_wait()
                folder_comp = self.request.split("\\")
                fine_folder_comp = folder_comp[:END]
                folder = "\\".join(fine_folder_comp)
                # self.copy_file(self.path_file, folder)  # so we don't trigger watchdog
                self.upload()
                # src_path = sys.argv[SECOND]
                # new_file = src_path.split(".")[START] + "." + format
                # Application.delete_file(new_file)

            self.sock.close()
        except Exception as msg:
            print("connection error:", msg)

    @staticmethod
    def get_request():
        """
        :return: the full file path (if whitespace is in the path)
        """
        params = sys.argv
        file_path = ""
        for x in range(STARTER, len(params)):
            if DOT in params[x]:
                file_path += " " + params[x]
                break
            file_path += " " + params[x]
        return file_path[SECOND:]  # get rid of blank space

    def get_ip_port(self):
        """
        :return: ip and port of server
        """
        for i in range(VALUE_COUNT):
            try:
                name, value, typ = EnumValue(self.server_key, i)
                if name == "IP":
                    ip = value
                if name == "port":
                    port = value
            except EnvironmentError:
                print("You have ", i, " values")
                break
        CloseKey(self.server_key)
        return ip, port

    @staticmethod
    def read_registry(department, reg_path, value_name):
        """
        :param reg_path: path to key
        :param value_name: key
        :return: the key's value
        """
        key = OpenKey(department, reg_path, REGISTRY_ZERO, KEY_READ)
        for i in range(BIG_NUMBER):
            try:
                name, value, typ = EnumValue(key, i)
                if name == value_name:
                    return value
            except EnvironmentError:
                print("You have ", i, " values")
                break
        CloseKey(key)
        return ""

    def without_cloud(self, request):
        """
        :return: converts a file path without client's cloud
        """
        new_request = request.replace(self.cloud, '')
        if new_request[START] == " ":
            return new_request[STARTER:]
        return new_request

    @staticmethod
    def valid_file(path):
        """
        checks if the path is a file that exists
        """
        if os.path.isfile(path):
            return True
        return False

    @staticmethod
    def delete_file(file_path):
        """
        deletes file
        """
        os.remove(file_path)

    @staticmethod
    def read_server_response(server_socket_choice):
        """
        reads the length and according to that, it reads the rest
        of the message
        """
        try:
            length_of_message = server_socket_choice.recv(BYTE).decode()
            if length_of_message.isdigit():
                return server_socket_choice.recv(int(length_of_message))
        except Exception as msg:
            print("at read_server_response:", msg)
            return SERVER_FELL

    @staticmethod
    def send_request_to_server(server_socket, request):
        """
        Send the request to the server.
        First the length of the request (2 digits), then the request itself
        Example: '04EXIT'
        Example: '12DIR c:\cyber'
        """
        server_socket. \
            send((str(len(request)).zfill(MSG_FILL) + request).encode())

    def download(self, format):
        """
        saves the given chunks to a file in the client
        """
        try:
            file = Application.new_format_path(self.request, format)
            new_location = Application.make_new_file_path(self.temp, file)
            # check if the file is valid
            check_len = self.sock.recv(BYTE).decode()
            check = self.sock.recv(int(check_len))
            if check != FILE_DOESNT_EXIST:
                self.client_reg.set_observer(DENY_OBS)
                client_file = open(new_location, 'wb')
                # write what we took out
                client_file.write(check)
                done = False
                while not done:
                    byte_message_len = self.sock.recv(BYTE)
                    length = byte_message_len.decode()
                    if length.isdigit():
                        real_len = int(length)
                        data = self.sock.recv(real_len)
                    if data == FILE_END:
                        done = True
                    else:
                        client_file.write(data)
                client_file.close()
                self.client_reg.set_observer(ALLOW_OBS)
                return new_location
            else:
                return 'nothing'
        except Exception as msg:
            print("at download:", msg)

    def copy_file(self, origin, dest):
        """
        :param origin: the original file path
        :param dest: the destination
        :return: -
        """
        shutil.copy2(origin, dest)

    def upload(self):
        """
        Sends a file from the server to the client
        """
        if Application.valid_file(self.path_file):
            self.client_reg.set_observer(DENY_OBS)
            client_file = open(self.path_file, 'rb')
            content = client_file.read(BYTE_NUMBER)
            while content != b'':
                Application.send_binary_response_to_server(content, self.sock)
                content = client_file.read(BYTE_NUMBER)
            client_file.close()
            Application.send_binary_response_to_server(FILE_END, self.sock)
            Application.delete_file(self.path_file)
            self.client_reg.set_observer(ALLOW_OBS)
            return Application.read_server_response(self.sock)
        else:
            Application.send_response_to_server(FILE_DOESNT_EXIST, self.sock)
            return FILE_DOESNT_EXIST

    @staticmethod
    def send_response_to_server(message, client_socket_ex):
        """
        sends the server the answer to what it input
        """
        message_length = len(message.encode())
        good_length = str(message_length).zfill(BYTE).encode()
        client_socket_ex.send(good_length + message.encode())

    @staticmethod
    def make_new_file_path(new_path, folder):
        """
        :param new_path: new path of file to merge
        :return: the new path
        """
        comp = folder.split("\\")
        return new_path + "\\" + comp[END]

    @staticmethod
    def new_format_path(path, format):
        """
        :param format: the new format
        :return: the same path but with new format
        """
        path_format = path.split('.')
        path_format[SECOND] = format
        return ".".join(path_format)

    @staticmethod
    def send_binary_response_to_server(message, client_socket_ex):
        """
        sends the server the answer to what it input
        """
        message_length = len(message)
        good_length = str(message_length).zfill(BYTE).encode()
        client_socket_ex.send(good_length + message)

    def start_file_and_wait(self):
        """
        :param fname: the file path - temporary
        :return: opens and continues when closed
        """
        lst1 = psutil.pids()
        p = subprocess.Popen([self.path_file], shell=True)
        print(p)
        time.sleep(LONG_SLEEP)
        lst2 = psutil.pids()
        lst3 = [p for p in lst2 if p not in lst1]

        still_alive = lst3
        while len(still_alive) > 0:
            self.send_response_to_server(self.username + SEPERATOR + WAIT, self.sock)
            live_p = psutil.pids()
            still_alive = [p for p in lst3 if p in live_p]
            time.sleep(SHORT_SLEEP)
        self.send_response_to_server(self.username + SEPERATOR + CONTINUE, self.sock)


app = Application()
