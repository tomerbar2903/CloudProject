"""
GUI for asking other users for sharing allowance.
"""


from ButtonFrame2 import *
from ShareGUI import *


class ChooseShareGUI(ButtonFrame2):
    """
    ask to have permission to take files from other
    users.
    """
    def __init__(self):
        """
        :param e: event handler
        """
        super().__init__(None, HOME_PAGE_TITLE, HOME_PAGE_TITLE,
                         ASK_FOR_SHARE_BTN, SHARE_BTN,
                         SYSTEM_REGISTER_PANEL_SIZE)
        self.btn2.Bind(wx.EVT_BUTTON, self.on_share)
        self.btn1.Bind(wx.EVT_BUTTON, self.on_ask)

    def on_ask(self, e):
        """
        :param e: event handler
        :return: show list of users in new GUI
        """


    def on_share(self, e):
        """
        :param e: event handler
        :return: shows list of my files to share
        """
        self.Close()
        ShareGUI()
