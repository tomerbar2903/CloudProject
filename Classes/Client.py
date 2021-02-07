import socket
import threading
import time
import os
import win32ui
import win32con
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
                self.req_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.req_socket.connect((self.ip, self.port))
                self.my_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                # connect to server
                self.my_socket.connect((self.ip, self.port))
                self.username = NO_USER
                self.password = NO_PASSWORD
                self.client_reg = ReadRegistry(CLIENT_REG)  # client reading
                self.cloud = self.client_reg. \
                    read_registry(HKEY_LOCAL_MACHINE,
                                  CLIENT_REG, CLOUD_REG)
            elif constructor_mode == APP_MODE:
                self.request = NO_COMMAND
                reg_ip = ReadRegistry(SERVER_REG)  # client reading
                self.client_reg = ReadRegistry(CLIENT_REG)  # client reading
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
                self.req_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.req_socket.connect((self.ip, self.port))
        except Exception as msg:
            print("at constructor Client", msg)

    def initiate_listen(self):
        """
        :return: sends the server an hello command
        """
        message = self.username + SEPERATOR + REQ_SOCK_COMMAND
        self.send_request_to_server(self.req_socket, message)
        receive_requests = threading.Thread(target=self.recieving_requests)
        receive_requests.start()

    def recieving_requests(self):
        """
        :return: recieveing requests and handles them
        """
        while True:
            request_length = self.req_socket.recv(BYTE).decode()
            if request_length.isdigit():
                request = self.req_socket.recv(int(request_length)).decode()
                req_and_prms = request.split(SEPERATOR)
                from_user = BLANK
                command = BLANK
                params = []
                if len(req_and_prms) > TWO_PARAMETER:
                    print("p1")
                    from_user = req_and_prms.pop(START)
                    print("from user", from_user)
                    command = req_and_prms.pop(START)
                    print("command", command)
                    params = req_and_prms
                    print("params", params)
                self.handle_server_request(from_user, command, params)

    def handle_server_request(self, from_user, command, params):
        """
        :return: handles request
        """
        if command in COMMANDS:
            if command == SHARE and \
                    len(params) == ONE_PARAMETER:
                self.client_reg.set_observer(DENY_OBS)
                file = File(params[START])
                real_file = file.get_name() + DOT + file.get_format()
                file_name = File(real_file).name + DOT + File(real_file).format
                message = from_user + " Wanted To Send You A File (" + file_name + ")"
                if win32ui.MessageBox(message, "Request Was Just Sent You", win32con.MB_YESNOCANCEL) == win32con.IDYES:
                    message_for_server = self.username + SEPERATOR + COPY_FILE + SEPERATOR + from_user + SEPERATOR\
                                         + self.without_cloud(file.path)
                    Client.send_request_to_server(self.my_socket, message_for_server)
                    name = Client.read_server_response(self.my_socket).decode()
                    file.set_name(name)
                    file_to_save = file.make_new_file_path(self.cloud)
                    Client.make_imaginary_file(file_to_save)
                    time.sleep(LONG_SLEEP)
                    self.client_reg.set_observer(ALLOW_OBS)
                    print("received")
                else:
                    print("doesnt work")
                    pass
                    # TODO - send server that request is not allowed

    def initiate_cloud(self):
        """
        :return: initiates cloud directory
        """
        if Client.valid_directory(self.cloud):
            ReadRegistry.set_registry(
                HKEY_LOCAL_MACHINE, CLIENT_REG, CLOUD_REG, self.cloud)
            return True
        return False

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

    def user_login(self, username, password):
        """
        :return: nothing if everything works correctly
        """
        self.send_request_to_server(
            self.my_socket, self.username +
            SEPERATOR + LOG_IN + SEPERATOR +
            username + SEPERATOR + password)
        reply = Client.read_server_response(self.my_socket)
        if reply.decode() != FINE:
            return reply.decode()
        self.username = username
        self.password = password
        ReadRegistry.set_registry(
            HKEY_LOCAL_MACHINE, CLIENT_REG, USERNAME_REG, self.username)
        ReadRegistry.set_registry(
            HKEY_LOCAL_MACHINE, CLIENT_REG, PASSWORD_REG, self.password)
        return FINE

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
                print("%s LOADING...." % file)
                ans = self.read_server_response(self.my_socket)
            self.upload(file, self.my_socket)

    def without_cloud(self, request):
        """
        :return: converts a file path without client's cloud
        """
        return request.replace(self.cloud, BLANK)

    @staticmethod
    def send_request_to_server(server_socket, request):
        """
        Send the request to the server.
        First the length of the request (4 digits), then the request itself
        Example: '0004EXIT'
        Example: '0012DIR c:\cyber'
        """
        print(request)
        server_socket. \
            send((str(len(request)).zfill(MSG_FILL) + request).encode())

    def answer_all(self, requests):
        """
        :param requests: a string of requests
        :return: deals with all of them
        """
        requests_list = requests.split(REQUEST_SEPARATOR)
        for request in requests_list:
            req = request.split(SEPERATOR)
            from_user = req[START]
            command = req[SECOND]
            params = []
            if len(req) >= TWO_PARAMETER:
                params = req[THIRD:]
            self.handle_server_request(from_user, command, params)

    def handle_user_input(self):
        """
        :return: does what the client asks for
        """
        done = False
        # checks for requests while was down
        message = self.username + SEPERATOR + GET_REQUESTS
        self.send_request_to_server(self.my_socket, message)
        requests = self.read_server_response(self.my_socket)
        if requests.decode() != NO_REQUESTS:
            self.answer_all(requests.decode())
        # while the operation is not quit. if quit - go out
        while not done:
            # if not blank command
            # sends the operation to the server
            data = self.read_server_response(self.my_socket)
            if data is not None:
                if data.decode() == READY:
                    data = self.upload(
                        self.request, self.my_socket)
                self.handle_server_response(data)
            if data != SERVER_FELL:
                pass
            else:
                self.my_socket.close()
                done = True

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
            if server_response.decode() != BLANK:
                if server_response != SERVER_FELL:
                    print(server_response.decode())
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

    def ask_for_share(self, user_to_ask):
        """
        :param user_to_ask: the username of the wanted user.
        :return: list of files of the user / 'permission denied' if doesnt allow
        """
        message = self.username + SEPERATOR + ASK_FOR_SHARE_BTN + SEPERATOR + user_to_ask
        Client.send_request_to_server(self.my_socket, message)
        reply = Client.read_server_response(self.my_socket)
        if reply != PERMISSION_DENIED:
            return reply
        return BLANK

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
                while content != BLANK.encode():
                    Client.send_binary_response_to_server(content, my_socket)
                    content = client_file.read(BYTE_NUMBER)
                client_file.close()
                Client.send_binary_response_to_server(FILE_END, my_socket)
                Client.delete_file(file_path)
                Client.make_imaginary_file(file_path)
                time.sleep(LONG_SLEEP)
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
