import socket
import time
import os
from File import *
from ReadRegistry import *


class Client(object):
    def __init__(self, constructor_mode, ip, port):
        """
        :param constructor_mode: 0- Known username (application & log in))
                                 1- Unknown username (set up)
        :param ip: optional
        :param port: optional
        :param request: optional
        """
        try:
            # initiate socket
            if constructor_mode == CLIENT_MODE:
                reg = ReadRegistry(SERVER_REG)  # server cloud
                ip1, port1 = reg.get_ip_port()
                if ip is not None and port is not None:
                    self.ip = ip
                    self.port = port
                else:
                    self.ip = ip1
                    self.port = port1
                self.request = NO_COMMAND
                self.my_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                # connect to server
                self.my_socket.connect((self.ip, self.port))
                self.username = NO_USER
                self.password = NO_PASSWORD
            elif constructor_mode == APP_MODE:
                self.request = NO_COMMAND
                reg_ip = ReadRegistry(SERVER_REG)  # client reading
                self.client_reg = ReadRegistry(CLIENT_REG)  # client reading
                self.client_reg.set_blup(ALLOW_BLUP)  # initiates
                self.client_reg.set_observer(ALLOW_OBS)  # initiates
                ip1, port1 = reg_ip.get_ip_port()
                if ip is not None and port is not None:
                    self.ip = ip
                    self.port = port
                else:
                    self.ip = ip1
                    self.port = port1
                self.username = self.client_reg. \
                    read_registry(HKEY_LOCAL_MACHINE,
                                  CLIENT_REG, USERNAME_REG)
                self.password = self.client_reg. \
                    read_registry(HKEY_LOCAL_MACHINE,
                                  CLIENT_REG, PASSWORD_REG)
                self.cloud = self.client_reg. \
                    read_registry(HKEY_LOCAL_MACHINE,
                                  CLIENT_REG, CLOUD_REG)
                self.my_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                # connect to server
                self.my_socket.connect((self.ip, self.port))
        except socket.error as msg:
            print("Connection failure: %request\n termination program" % msg)

    def initiate_cloud(self):
        """
        :return: initiates cloud directory
        """
        if Client.valid_directory(self.cloud):
            ReadRegistry.set_registry(
                HKEY_LOCAL_MACHINE, CLIENT_REG, CLOUD_REG, self.cloud)
            return True
        return False

    @staticmethod
    def get_server_details():
        """
        returns the ip and port of client for app
        """
        reg = ReadRegistry(SERVER_REG, r"E:\12\bla.txt")
        return reg.get_ip_port()

    def user_setup(self, username, password):
        """
       :return: sets the username and pass word to database
        """
        self.send_request_to_server(self.my_socket,
                                    self.username + SEPERATOR +
                                    NEW_USER + SEPERATOR + username +
                                    SEPERATOR + password)
        reply = Client.read_server_response(self.my_socket)
        if reply.decode() == USER_ADDED:
            self.username = username
            self.password = password
            ReadRegistry.set_registry(
                HKEY_LOCAL_MACHINE, CLIENT_REG, USERNAME_REG, self.username)
            ReadRegistry.set_registry(
                HKEY_LOCAL_MACHINE, CLIENT_REG, PASSWORD_REG, self.password)
            return True
        return True

    def user_login(self, username, password):
        """
        :return: nothing if everything works correctly
        """
        self.send_request_to_server(
            self.my_socket, self.username +
                            SEPERATOR + LOG_IN + SEPERATOR +
                            username + SEPERATOR + password)
        reply = Client.read_server_response(self.my_socket)
        if reply.decode() == INCORRECT_PASSWORD:
            return False
        self.username = username
        self.password = password
        ReadRegistry.set_registry(
            HKEY_LOCAL_MACHINE, CLIENT_REG, USERNAME_REG, self.username)
        ReadRegistry.set_registry(
            HKEY_LOCAL_MACHINE, CLIENT_REG, PASSWORD_REG, self.password)
        return True

    def set_up(self):
        """
        creates a new directory under C:\Program Files - where temporary
        files will be held
        :return: -
        """
        if not os.path.isdir(self.cloud + APPINFO):
            os.mkdir(self.cloud + APPINFO)

    def upload_all(self):
        """
        :return: uploads all files to the cloud
        """
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.cloud):
            if APPINFO not in r:
                for file in f:
                    if File(file).get_format() != CLOUD_FORMAT:
                        files.append(os.path.join(r, file))
        for file in files:
            req = self.username + SEPERATOR + \
                  UPLOAD_FILE + SEPERATOR + self.without_cloud(file)
            self.send_request_to_server(self.my_socket, req)
            ans = self.read_server_response(self.my_socket)
            while not ans.decode() == READY:
                time.sleep(SHORT_SLEEP)
                print(ans)
                ans = self.read_server_response(self.my_socket)
            self.upload(file, self.my_socket)

    def without_cloud(self, request):
        """
        :return: converts a file path without client's cloud
        """
        return request.replace(self.cloud, '')

    @staticmethod
    def send_request_to_server(server_socket, request):
        """
        Send the request to the server.
        First the length of the request (2 digits), then the request itself
        Example: '04EXIT'
        Example: '12DIR c:\cyber'
        """
        print(request)
        server_socket. \
            send((str(len(request)).zfill(MSG_FILL) + request).encode())

    def handle_user_input(self):
        """
        :return: does what the client asks for
        """
        done = False
        data = str(2)  # starting value
        # while the operation is not quit. if quit - go out
        while not done:

            # if not blank command
            req_and_prm = self.request.split()
            command = req_and_prm[START]
            ok = self.valid_request()
            if ok:
                time.sleep(SHORT_SLEEP)
                # sends the operation to the server
                if self.client_reg.\
                        read_registry(HKEY_LOCAL_MACHINE,
                                      CLIENT_REG, BLUP_REG) == ALLOW_BLUP:
                    self.send_request_to_server(
                        self.my_socket,
                        self.username + SEPERATOR + self.request)

                    data = self.read_server_response(self.my_socket)
                    if data.decode() == READY:
                        data = self.upload(
                            req_and_prm[END], self.my_socket).encode()
                    self.handle_server_response(data)
            else:  # prints the message accordingly
                if type(ok) == bool:
                    print("you entered a non valid value")
                else:
                    print(ok)
            if command.upper() != 'EXIT' and data != SERVER_FELL:
                pass
            else:
                self.my_socket.close()
                done = True

    def valid_request(self):
        """
        :param request: the client'request request
        :return: if the request is valid or not
        """
        req_and_prms = self.request.split()
        command = req_and_prms[START]
        if command.upper() in COMMANDS:
            if command.upper() == UPLOAD_FILE and \
                    len(req_and_prms) == TWO_PARAMETER:
                return True
            elif command.upper() == NO_COMMAND:
                return True
            else:
                return FILE_DOESNT_EXIST
        return False

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
    def handle_server_response(server_response):
        """
        :param server_response: the server'request response
        :return: handles the response
        """
        try:
            if server_response.decode() != "":
                if server_response != SERVER_FELL:
                    print("print bytes: ", server_response)
                    print("print string: ", server_response.decode())
                else:
                    print("\n\n******the server has fallen down******\n")
        except Exception as msg:
            print("at handle_server_response:", msg)

    @staticmethod
    def valid_file(path):
        """
        checks if the path is a file that exists
        """
        if os.path.isfile(path):
            return True
        return False

    @staticmethod
    def send_response_to_server(message, client_socket_ex):
        """
        sends the server the answer to what it input
        """
        message_length = len(message.encode())
        good_length = str(message_length).zfill(BYTE).encode()
        client_socket_ex.send(good_length + message.encode())

    @staticmethod
    def send_binary_response_to_server(message, client_socket_ex):
        """
        sends the server the answer to what it input
        """
        message_length = len(message)
        good_length = str(message_length).zfill(BYTE).encode()
        client_socket_ex.send(good_length + message)

    def upload(self, file_path, my_socket):
        """
        Sends a file from the server to the client
        """
        if Client.valid_file(file_path):
            self.client_reg.set_observer(DENY_OBS)
            if File(file_path).get_format() != CLOUD_FORMAT:
                client_file = open(file_path, 'rb')
                content = client_file.read(BYTE_NUMBER)
                while content != b'':
                    Client.send_binary_response_to_server(content, my_socket)
                    content = client_file.read(BYTE_NUMBER)
                client_file.close()
                Client.send_binary_response_to_server(FILE_END, my_socket)
                Client.delete_file(file_path)
                Client.make_imaginary_file(file_path)
                self.client_reg.set_observer(ALLOW_OBS)
                return Client.read_server_response(my_socket)
            else:
                return FILE_ALREADY_IN_CLOUD
        else:
            Client.send_response_to_server(FILE_DOESNT_EXIST, my_socket)
            return FILE_DOESNT_EXIST

    @staticmethod
    def delete_file(file_path):
        """
        deletes file
        """
        os.remove(file_path)

    @staticmethod
    def make_imaginary_file(file_path):
        """
        :param file_path: the file we want to be imaginary
        :return: -
        """
        new_file_path = File(file_path)
        new_file_path = new_file_path.change_file_to_cloud(CLOUD_FORMAT)
        i_file = open(new_file_path, 'wb')
        i_file.close()

    @staticmethod
    def valid_directory(folder):
        """
        :param folder: wanted folder
        :return: True - exists, False - otherwise
        """
        return os.path.isdir(folder)
