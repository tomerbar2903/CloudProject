"""
The Register (LOG IN \ SIGN UP) Panel
"""


from ButtonFrame2 import *
from SystemRegisterGUI import *


class RegisterGUI(ButtonFrame2):
    """
    initiates window
    """
    def __init__(self):
        """
        initiates the panel - title and buttons
        """
        super().__init__(None, REGISTER_TITLE, SELECT,
                         SIGN_UP_BTN, LOG_IN_BTN, SIGN_IN_PANEL_SIZE)
        self.bind_buttons()
        self.Show()

    def bind_buttons(self):
        """
        :return: opens the correct window
        """
        self.btn1.Bind(wx.EVT_BUTTON, self.open_sign_up)
        self.btn2.Bind(wx.EVT_BUTTON, self.open_log_in)

    def open_log_in(self, e):
        """
        :return: closes current panel and opens up a new
        window of registering
        """
        self.Close()
        self.folder_manager.client.my_socket.close()  # avoiding overflow
        log_in_panel = SystemRegisterGUI(None, LOG_IN_BTN)
        log_in_panel.Show()

    def open_sign_up(self, e):
        """
        :return: closes current panel and opens up a new
        window of registering
        """
        self.Close()
        self.folder_manager.client.my_socket.close()  # avoiding overflow
        sign_up_panel = SystemRegisterGUI(None, SIGN_UP_BTN)
        sign_up_panel.Show()
