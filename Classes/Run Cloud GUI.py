"""
runs the GUI program of registering
"""


from RegisterPanel import *


def main():
    """
    runs GUI
    """
    app = wx.App()
    RegisterGUI()
    app.MainLoop()


if __name__ == '__main__':
    main()
