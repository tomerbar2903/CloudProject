"""
runs the GUI program of registering
"""


from RegisterPanel import *
from SystemRegisterGUI import *
from ShareGUI import *


def main():
    """
    runs GUI
    """
    c = MyHandler(CLIENT_MODE)
    app = wx.App()
    RegisterGUI(c.client)
    app.MainLoop()


if __name__ == '__main__':
    main()
