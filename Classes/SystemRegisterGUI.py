"""
The panel where you enter your username and password (LOG IN \ SIGN UP)
"""


import threading
from GeneralGUI import *
from Folder_Manager import *
from InitCloudGUI import *
from ChooseShareGUI import *
from ShareGUI import *
import subprocess


CLIENT_PROGRAM_PATH = R'E:\\12\\Project\\Classes\\Folder_Manager.py'


class SystemRegisterGUI(GeneralGUI):
    """
    enter username & password - connect to server
    """
    def __init__(self, mode, client):
        """
        :param mode: LOG IN \ SIGN UP
        """
        super().__init__(None, mode, SYSTEM_REGISTER_PANEL_SIZE, client)
        self.mode = mode
        self.username_static = wx.StaticText(self.pnl, label=USERNAME_STATIC)
        self.password_static = wx.StaticText(self.pnl, label=PASSWORD_STATIC)
        self.user_txt = wx.TextCtrl(self.pnl)
        self.password_txt = wx.TextCtrl(self.pnl)
        self.btn1 = wx.Button(self.pnl, label=mode)
        self.user_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.positions()
        self.btn1.Bind(wx.EVT_BUTTON, self.on_submit)
        self.Show()

    def on_submit(self, e):
        """
        :return: checks the log in \ sign up method
        """
        username = self.user_txt.GetLineText(0)
        password = self.password_txt.GetLineText(0)
        self.Close()
        if self.mode == LOG_IN_BTN:
            r = self.client.user_login(username,
                                       password)
            if r == FINE:
                wx.MessageBox('Logged In', 'Register', wx.OK | wx.ICON_INFORMATION)
                client_thread = threading.Thread(
                    target=self.run_client)
                client_thread.start()
                ChooseShareGUI(self.client.username, self.client)
            else:
                wx.MessageBox(r, "Register", wx.OK | wx.ICON_INFORMATION)
                SystemRegisterGUI(self.mode, self.client)  # Opens up a new window
        elif self.mode == SIGN_UP_BTN:
            r = self.client.user_setup(username,
                                       password)
            if r:
                wx.MessageBox('New Account Is Ready To Go!', 'Register', wx.OK | wx.ICON_INFORMATION)
                InitCloudGUI(self.client)
            else:
                wx.MessageBox('Username Already Exists', "Register", wx.OK | wx.ICON_INFORMATION)
                SystemRegisterGUI(self.mode, self.client)  # Opens up a new window

    def run_client(self):
        """
        :return: runs client in a thread
        """
        subprocess.run([PYTHON, CLIENT_PROGRAM_PATH, APP_MODE])
        self.client.client_reg.set_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, FOLDER_MANAGER_REG, NO_REG)

    def positions(self):
        """
        :return: puts to positions
        """
        self.user_sizer.Add(window=self.username_static, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        self.user_sizer.Add(window=self.user_txt, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        self.password_sizer.Add(window=self.password_static, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        self.password_sizer.Add(window=self.password_txt, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        self.btn_sizer.Add(window=self.btn1, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        self.sizer.Add(self.user_sizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        self.sizer.Add(self.password_sizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        self.sizer.Add(self.btn_sizer, proportion=0, flag=wx.ALL | wx.CENTER, border=5)
        self.SetSizer(self.sizer)
