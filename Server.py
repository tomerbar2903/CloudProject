import socket
import os
from File import *
import threading
from ReadRegistry import *
import shutil
import sqlite3
import time

SHORT_SLEEP = 1
LONG_SLEEP = 3
DATABASE = R"E:\12\Project\Usernames.db"
IP = '0.0.0.0'


class Server(object):
    def __init__(self, ip, port):
        """
        initiates the server
        :param ip: ip
        :param port: port
        """
        try:
            self.ip = ip
            self.port = port
            reg = ReadRegistry(SERVER_REG)  # server reading
            self.cloud = reg.get_cloud()
            self.server_socket = self.initiate_server_socket()
            self.clients = START_COUNT
            self.lock = threading.Lock()
        except socket.error as msg:
            print("Connection failure: %s\n terminating program" % msg)

    def setup(self, username):
        """
        :return: sets trash can
        """
        if not os.path.isdir(self.cloud + "\\" + username + "\\" + "\\Trash"):
            os.mkdir(self.cloud + "\\" + username + "\\" + "\\Trash")

    def initiate_server_socket(self):
        """
        makes a server that can listen to 1 client at a time
        """
        try:
            # opens the server socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.ip, self.port))

            # can listen to only 1 client at a time
            server_socket.listen(1)
            return server_socket
        except Exception as msg:
            print("at initiate_server_socket:", msg)
        except socket.error as msg:
            print("socket error at initiate_server_socket:", msg)

    def handle_clients(self):
        """
        a function that handles requests from multiple clients
        """
        # so that it will go into the loop
        done = False

        while done is not True:
            try:
                # accepting a connect request
                client_socket, address = self.server_socket.accept()

                # handles one client and its message
                client_thread = threading.Thread(
                    target=self.handle_single_client,
                    args=(client_socket,))
                client_thread.start()
            except socket.error as msg:
                print("error at handle client:", msg)

    @staticmethod
    def receive_client_request(client_socket):
        """
        returns the parameters and commands from client
        """
        message_length = client_socket.recv(BYTE).decode()
        if message_length.isdigit():
            message = client_socket.recv(int(message_length))
            request = message.decode()
            # split to request and parameters
            req_and_prms = request.split(SEPERATOR)
            username = req_and_prms.pop(START)
            command = req_and_prms[START]
            if len(req_and_prms) > ONE_PARAMETER:
                return username, command, req_and_prms[PRM:]
            else:
                return username, command, []  # no parameters
        else:
            return "", "", []  # illegal size parameter

    def check_client_request(self, username, request, params):
        """
        :param request: the request from client
        :param params: the parameters that come with the request
        :return: if the total request is valid
        """
        try:
            if request.upper() in COMMANDS:

                if request.upper() == UPLOAD_FILE and \
                        len(params) == ONE_PARAMETER:
                    if not Server.valid_file(params[START]):
                        return True
                    else:
                        return FILE_DOESNT_EXIST
                elif request.upper() == DOWNLOAD_FILE and \
                        len(params) == ONE_PARAMETER:
                    if self.check_file_name(username, params[START]):
                        return True
                    else:
                        return NOT_IN_CLOUD
                elif request.upper() == MAKE_DIR and \
                        len(params) <= ONE_PARAMETER:
                    return True
                elif request.upper() == NO_COMMAND:
                    return True
                elif request.upper() == DELETE_FILE and \
                        len(params) == ONE_PARAMETER:
                    return True
                elif request.upper() == NEW_USER and \
                        len(params) == TWO_PARAMETER:
                    return True
                elif request.upper() == LOG_IN and \
                        len(params) == TWO_PARAMETER:
                    return True
                elif request.upper() == MOVE_FILE and \
                        len(params) == THREE_PARAMETER:
                    return True
                elif request.upper() == MAKE_DIR and \
                        len(params) == ONE_PARAMETER:
                    return True
                elif request.upper() == MOVE_DIR and \
                        len(params) == TWO_PARAMETER:
                    return True
            return False
        except Exception as m:
            print("at check_client_request", m)

    def create_dirs(self, username, req):
        """
        :return: creates initial directories
        """
        path = self.cloud + "\\" + username + "\\" + req
        if not os.path.isdir(path):
            os.mkdir(path)

    @staticmethod
    def get_file_path(file_path):
        """
        :param file_path: the path of the file
        :return: the path without file
        """
        file_comp = file_path.split("\\")
        new_file_path = "\\".join(file_comp[:END])
        return new_file_path

    def check_file_name(self, username, file_path):
        """
        :param file_path: the file of the client's file
        :return: true \ false if file name exists in cloud
        """
        try:
            file_path = File(self.cloud + "\\" + username + "\\" + file_path)
            file_name = file_path.get_name()
            directory = Server.get_file_path(file_path.path)
            cloud_files = os.listdir(directory)
            for i in range(len(cloud_files)):
                cloud_files[i] = File(cloud_files[i]).get_name()
            if file_name in cloud_files:
                return True
            return False
        except Exception as m:
            print("at check_file_name", m)

    def handle_single_client(self, client_socket):
        """
        handles only one costumer. returns what the client wants according the
        instructions
        """
        # thread setting
        num = self.clients
        self.clients += 1
        print("starting thread", num)

        try:
            # so that at first, it will get into the loop
            done2 = False
            reply = ""  # initiates
            while not done2:
                # gets the message from the client
                username, request, params = Server.receive_client_request(
                    client_socket)

                # checks if the input from the client is fine
                ok = self.check_client_request(username, request, params)
                if ok:
                    # holds the value of the answer to the client
                    answer = self. \
                        handle_client_request(username, request, params)

                    if answer == READY:  # ready to download
                        Server.send_response_to_client(answer, client_socket)
                        answer = self.download(username, params[END],
                                               client_socket)
                    elif answer == OK:  # ready to upload
                        format = self.get_format(username, params[START])
                        Server.send_response_to_client(format, client_socket)
                        answer = Server.upload(username, params[END], format,
                                               client_socket, self.cloud)
                        path = params[END]
                        real_path_format = path.split(DOT)[:END]
                        real_path_format.append(format)
                        original_file = DOT.join(real_path_format)
                        reply = self.receive_client_request(
                            client_socket)[SECOND]
                        while reply == WAIT:
                            time.sleep(SHORT_SLEEP)
                            reply = self.receive_client_request(
                                client_socket)[SECOND]
                        if reply == CONTINUE:
                            ans = self.download(
                                username, original_file, client_socket)
                        else:
                            print("error at re-uploading")
                    elif request == DELETE_FILE:
                        username2, request2, params2 = \
                            self.receive_client_request(client_socket)
                        # waits for create file command
                        if MOVE_FILE in request2:
                            params2.append(answer)
                        else:
                            Server.delete_file(answer)
                        # sends the original file path
                        answer = self.handle_client_request(
                            username2, request2, params2)
                else:
                    # if the client entered something not from the protocol
                    if type(ok) == bool:
                        if reply == CONTINUE:
                            answer = BLANK
                        else:
                            answer = NONE_VALID
                    else:
                        answer = ok
                # sends the general message to the client
                Server.send_response_to_client(answer, client_socket)
        except socket.error as msg:
            print("A client has left or app finished", msg)
            self.clients -= ADDER
            return False
        except Exception as msg:
            print("general error at handle_single_client:", msg)
            return False

    def handle_client_request(self, username, request, params):
        """
        returns the wanted values, according to the client's request
        """
        try:
            if request.upper() == UPLOAD_FILE:
                return READY
            elif request.upper() == DOWNLOAD_FILE:
                return OK
            elif request.upper() == NO_COMMAND:
                return BLANK
            elif request.upper() == MAKE_DIR:
                if len(params) > NO_PARAMETERS:
                    self.create_dirs(username, params[START])
                    return BLANK
                return NO_DIR_ADDED
            elif request.upper() == DELETE_FILE:
                new_path = self.find_file(username, params[START])
                trash = self.cloud + "\\" + username + "\\Trash"
                shutil.move(new_path, trash)
                dest_path = File(new_path).make_new_file_path(trash)
                return dest_path
            elif request.upper() == NEW_USER and username == NO_USER:
                return self.check_sign_up(params[START], params[SECOND])
            elif request.upper() == LOG_IN and username == NO_USER:
                return Server.check_log_in(params[START], params[SECOND])
            elif request.upper() == RE_UPLOAD_FILE:
                return YAY
            elif request.upper() == MOVE_FILE:
                origin = params[SECOND]
                dest = self.cloud + "\\" + username + params[START]
                # erases the file name and format
                dest = "\\".join(dest.split("\\")[:END])
                shutil.move(origin, dest)
                return ""
            elif request.upper() == MAKE_DIR:
                return self.make_dir(params[START])
            elif request.upper() == MOVE_DIR:
                os.rename(self.cloud + "\\" + username + "\\" + params[START],
                          self.cloud + "\\" + username + "\\" + params[SECOND])
                return BLANK
            return False
        except Exception as m:
            print("at handle_client_request:", m)

    def make_dir(self, dire):
        """
        :return: makes the directory in server
        """
        os.mkdir(self.cloud + dire)
        return ""

    @staticmethod
    def check_log_in(username, pw):
        """
        :param username: -
        :param pw: password
        :return: checks if details are correct
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            users = cur.execute(DB_COMMAND_USERS)
            ok = False
            for user in users:
                if user[START] == username:
                    if user[SECOND] == str(pw):
                        ok = True
                    else:
                        return INCORRECT_PASSWORD
            if ok:
                return FINE
            else:
                return SOMETHING_WENT_WRONG
            conn.close()
        except Exception as m:
            print("at check_log_in", m)

    def check_sign_up(self, username, password):
        """
        :param  username: the wanted username
                password: the password
        :return: added - not in current database, not added if already exists
        """
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        users = cur.execute(DB_COMMAND_USERNAME)
        ok = False
        for user in users:
            if user[START] == username:
                ok = True
        if ok:
            return USERNAME_EXISTS
        else:
            p_and_u = [username, password]
            query = "INSERT INTO users(username, password) values (?, ?)"
            cur.execute(query, p_and_u)
            conn.commit()
            os.mkdir(self.cloud + "\\" + username)
            self.setup(username)
            ans = USER_ADDED
        conn.close()
        return ans

    def find_file(self, username, client_file_path):
        """
        :param client_file_path: the incomplete file
        :return: the existing file in server
        """
        try:
            f = self.get_format(username, client_file_path)
            return self.cloud + "\\" + username + "\\" + \
                client_file_path.split(DOT)[START] + DOT + f
        except Exception as m:
            print("at find_file", m)

    @staticmethod
    def send_response_to_client(message, client_socket):
        """
        sends the client the answer to what it input
        """
        message_length = len(message.encode())
        good_length = str(message_length).zfill(BYTE).encode()
        client_socket.send(good_length + message.encode())

    @staticmethod
    def send_binary_response_to_client(message, client_socket):
        """
        sends the client the answer to what it input
        """
        message_length = len(message)
        good_length = str(message_length).zfill(BYTE).encode()
        client_socket.send(good_length + message)

    @staticmethod
    def valid_file(path):
        """
        checks if the path is a file that exists
        """
        if os.path.isfile(path):
            return True
        return False

    def get_format(self, username, file_path):
        """
        :param file_path: the path of the file in the client
        :return: the format of the original file
        """
        try:
            folder = '\\'.join(file_path.split('\\')[:END])
            file_list = os.listdir(
                self.cloud + "\\" + username + "\\" + folder)
            files = []
            for i in range(len(file_list)):
                if DOT in file_list[i]:
                    files.append(File(file_list[i]))
            names_and_formats = {}
            for file in files:
                names_and_formats[file.get_name()] = file.get_format()
            file_path = File(file_path)
            file_name = file_path.get_name()
            if file_name in names_and_formats.keys():
                return names_and_formats[file_name]
            return ERROR_FORMAT
        except Exception as m:
            print("at get_format", m)

    def download(self, username, request, my_socket):
        """
        saves the given chunks to a file in the cloud
        """
        try:
            new_location = self.cloud + "\\" + username + "\\" + request
            # check if the file is valid
            if os.path.isfile(new_location):
                Server.delete_file(new_location)
            check_len = my_socket.recv(BYTE).decode()
            check = my_socket.recv(int(check_len))
            if check != FILE_DOESNT_EXIST:
                client_file = open(new_location, 'wb')
                # write what we took out
                client_file.write(check)
                done = False
                while not done:
                    byte_message_len = my_socket.recv(BYTE)
                    length = byte_message_len.decode()
                    if length.isdigit():
                        real_len = int(length)
                        data = my_socket.recv(real_len)
                    if data == FILE_END:
                        done = True
                    else:
                        client_file.write(data)
                client_file.flush()
                client_file.close()
                return FILE_SENT
            else:
                return FILE_DOESNT_EXIST
        except Exception as m:
            print("at download", m)

    @staticmethod
    def delete_file(file_path):
        """
        deletes file
        """
        os.remove(file_path)

    @staticmethod
    def upload(username, file_path, format, client_socket, c):
        """
        Sends a file from the server to the client
        """
        try:
            file_path = File(c + "\\" + username + "\\" + file_path)
            real_file = file_path.new_format_path(format)
            if Server.valid_file(real_file):
                server_file = open(real_file, 'rb')
                content = server_file.read(BYTE_NUMBER)
                while content != BLANK.encode():
                    Server.send_binary_response_to_client(
                        content, client_socket)
                    content = server_file.read(BYTE_NUMBER)
                    server_file.flush()
                server_file.close()
                Server.send_binary_response_to_client(FILE_END, client_socket)
                return FILE_SENT
            else:
                Server.send_response_to_client(
                    FILE_DOESNT_EXIST, client_socket)
                return FILE_DOESNT_EXIST
        except Exception as m:
            print("at upload", m)


s = Server(IP, PORT)
s.handle_clients()
