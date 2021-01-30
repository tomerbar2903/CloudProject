"""
The Register (LOG IN \ SIGN UP) Panel
"""


from ButtonFrame2 import *
from SystemRegisterGUI import *


class RegisterGUI(ButtonFrame2):
    """
    initiates window
    """
    def __init__(self, client):
        """
        initiates the panel - title and buttons
        """
        super().__init__(None, REGISTER_TITLE, SELECT,
                         SIGN_UP_BTN, LOG_IN_BTN, SIGN_IN_PANEL_SIZE, client)
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
        SystemRegisterGUI(LOG_IN_BTN, self.client)

    def open_sign_up(self, e):
        """
        :return: closes current panel and opens up a new
        window of registering
        """
        self.Close()
        SystemRegisterGUI(SIGN_UP_BTN, self.client)
