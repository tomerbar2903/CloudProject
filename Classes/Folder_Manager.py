"""
handles client's file system changes
"""

from Client import *
import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def __init__(self, con_mode):
        """
        initiates folder manager
        con_mode - for client
        """
        self.reg = ReadRegistry(CLIENT_REG)
        self.client = Client(con_mode, None, None)  # regular client

    def on_created(self, event):
        """
        :param event: new file / folder created
        :return: uploads new file to cloud
        """
        time.sleep(SHORT_SLEEP)
        print(event.src_path, "created")
        new_file = event.src_path
        observer_check = self.reg.read_registry(HKEY_LOCAL_MACHINE,
                                                CLIENT_REG, OBSERVER)
        last_deleted = self.reg.read_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, DELETE_FLAG_REG)
        if observer_check == ALLOW_OBS:
            if APPLICATION_GUI_NAME not in new_file and PROJECT_FILES not in new_file:
                if last_deleted != File(new_file).name:
                    new_file = File.validate_file(new_file, RENAME_FILE_MODE)
                if Client.valid_file(new_file) and \
                        File(new_file).get_format() != CLOUD_FORMAT and \
                        APPINFO not in new_file:
                    self.client.send_request_to_server(self.client.my_socket,
                                                       self.client.username +
                                                       SEPERATOR + UPLOAD_FILE +
                                                       SEPERATOR +
                                                       self.client.without_cloud(
                                                           new_file))
                    self.client.request = new_file
                elif File(new_file).get_format() == CLOUD_FORMAT and \
                        DOT in new_file and APPINFO not in new_file:
                    self.client.send_request_to_server(self.client.my_socket,
                                                       self.client.username +
                                                       SEPERATOR +
                                                       MOVE_FILE + SEPERATOR +
                                                       self.client.without_cloud(
                                                           new_file))
                elif DOT not in new_file:
                    self.client.send_request_to_server(self.client.my_socket,
                                                       self.client.username +
                                                       SEPERATOR +
                                                       MAKE_DIR + SEPERATOR +
                                                       self.client.without_cloud(
                                                           new_file))

    def on_deleted(self, event):
        """
        :param event: detects file or dir deletion
        :return: changes file system in cloud
        """
        print(event.src_path, "deleted")
        format = File(event.src_path).get_format()
        observer_check = self.reg.read_registry(HKEY_LOCAL_MACHINE,
                                                CLIENT_REG, OBSERVER)
        if observer_check == ALLOW_OBS:
            if APPLICATION_GUI_NAME not in event.src_path and PROJECT_FILES not in event.src_path:
                if DOT in event.src_path and APPINFO not in event.src_path \
                        and format == CLOUD_FORMAT:
                    self.client.send_request_to_server(
                        self.client.my_socket, self.client.username +
                                               SEPERATOR + DELETE_FILE + SEPERATOR +
                                               self.client.without_cloud(event.src_path))
                    self.reg.set_delete_flag(File(event.src_path).name)

    def on_moved(self, event):
        """
        :param event: file system change
        :return: name changed (file/directory)
        """
        print(event.src_path, event.dest_path, "moved or changed name")
        src = event.src_path
        dest = event.dest_path
        observer_check = self.reg.read_registry(HKEY_LOCAL_MACHINE,
                                                CLIENT_REG, OBSERVER)
        if observer_check == ALLOW_OBS:
            if APPLICATION_GUI_NAME not in event.src_path and PROJECT_FILES not in event.src_path:
                if DOT not in src and DOT not in dest:
                    self.client.send_request_to_server(
                        self.client.my_socket, self.client.username +
                                               SEPERATOR + MOVE_DIR + SEPERATOR +
                                               self.client.without_cloud(src) + SEPERATOR +
                                               self.client.without_cloud(dest))

    def get_working_dir(self):
        """
        :return: the cloud directory
        """
        return self.client.cloud

    def handle_client_input(self):
        """
        :return: manages client
        """
        self.client.handle_user_input()

    def send_initial_system(self):
        """
        :return: sends the server the initial structure of
                 the client's file system
        """
        dir_list = [x[START] for x in os.walk(self.client.cloud)]
        for f in dir_list:
            if f != self.client.cloud and f != self.client.cloud + APPINFO and (self.client.cloud + "\\" +
                                                                                PROJECT_FILES_CHECK) not in f:
                path = self.client.without_cloud(f)
                self.client.send_request_to_server(
                    self.client.my_socket, self.client.username +
                                           SEPERATOR + MAKE_DIR + SEPERATOR + path)
        print("file system downloaded")


if __name__ == "__main__":
    mode = sys.argv[SECOND]
    event_handler = MyHandler(mode)
    observer = Observer()
    observer.schedule(
        event_handler, path=event_handler.get_working_dir(),
        recursive=True)
    event_handler.send_initial_system()
    event_handler.client.upload_all()
    observer.start()
    event_handler.handle_client_input()

    try:
        while True:
            time.sleep(SHORT_SLEEP)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    event_handler.reg.set_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, FOLDER_MANAGER_REG, NO_REG)
