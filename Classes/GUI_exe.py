"""
An exe file to open the GUI
"""


from RegisterPanel import *
from ChooseShareGUI import *
from Client import *
import threading
from ReadRegistry import *


class GuiExe(object):
    """
    reads registry and opens the gui accordingly
    """
    def __init__(self):
        self.reg = ReadRegistry(CLIENT_REG)
        self.username = self.reg.read_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, USERNAME_REG)
        self.password = self.reg.read_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, PASSWORD_REG)
        if self.username == BLANK and self.password == BLANK:
            self.client = Client(CLIENT_MODE, None, None)
            app = wx.App()
            RegisterGUI(self.client)
            app.MainLoop()
        else:
            self.client = Client(MID_GUI_MODE, None, None)
            app = wx.App()
            folder_manager = self.reg.read_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, FOLDER_MANAGER_REG)
            if folder_manager == NO_REG:
                client_thread = threading.Thread(
                    target=self.run_client)
                client_thread.start()
            ChooseShareGUI(self.username, self.client)
            app.MainLoop()

    def run_client(self):
        """
        :return: runs client in a thread
        """
        subprocess.run([PYTHON, CLIENT_PROGRAM_PATH, APP_MODE])
        self.client.client_reg.set_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, FOLDER_MANAGER_REG, NO_REG)


def main():
    """
    creates gui object
    """
    GuiExe()


if __name__ == '__main__':
    main()
