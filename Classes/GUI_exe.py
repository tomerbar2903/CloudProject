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
        self.client = Client(CLIENT_MODE, None, None)
        if self.username == BLANK and self.password == BLANK:
            app = wx.App()
            RegisterGUI(self.client)
            app.MainLoop()
        else:
            app = wx.App()
            SystemRegisterGUI(LOG_IN_BTN, self.client)
            app.MainLoop()


def main():
    """
    creates gui object
    """
    GuiExe()


if __name__ == '__main__':
    main()
