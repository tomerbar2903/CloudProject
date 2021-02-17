"""
The class for initiating the cloud path after sign up
"""


from ButtonFrame2 import *
from CONSTS import *
import subprocess
import threading
from ShareGUI import *
from ChooseShareGUI import *


class InitCloudGUI(GeneralGUI):
    """
    creating the panel
    """
    def __init__(self, client):
        """
        initiating the panel
        """
        super().__init__(None, SELECT_DIRECTORY, INIT_CLOUD_GUI_SIZE, client)
        self.browser = None
        self.static_txt = wx.StaticText(self.pnl, label=CHOOSE_YOUR_CLOUD_STATIC)
        self.submit_btn = wx.Button(self.pnl, label=SUBMIT_BTN)
        self.submit_btn.Bind(wx.EVT_BUTTON, self.on_submit)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.browse()
        self.order()
        self.Show()

    def on_submit(self, e):
        """
        :param check: if the selected directory is fine
        :return: -
        """
        self.client.cloud = self.browser.GetPath()
        self.Close()
        if self.client.cloud == BLANK:
            wx.MessageBox("You Must Choose A Folder To Continue!", 'Set-Up', wx.OK | wx.ICON_INFORMATION)
            InitCloudGUI(self.client)
        f = self.client.initiate_cloud()
        if not f:
            InitCloudGUI(self.folder_client.client)
        else:
            self.client.set_up()
            wx.MessageBox("You Are All Set!", 'Set-Up', wx.OK | wx.ICON_INFORMATION)
            client_thread = threading.Thread(
                target=self.run_client)
            client_thread.start()
            ChooseShareGUI(self.client.username, self.client)

    def run_client(self):
        """
        :return: runs client in a thread
        """
        subprocess.run([PYTHON, self.client.cloud + APPINFO + "\\Folder_Manager.py", APP_MODE])

    def browse(self):
        """
        :return: the user can browse and select a folder
        """
        self.browser = wx.DirPickerCtrl()
        self.browser.Create(self.pnl, path=BLANK, pos=wx.DefaultPosition, size=wx.DefaultSize,
                            style=wx.DIRP_DEFAULT_STYLE, name=wx.DirPickerCtrlNameStr)

    def order(self):
        """
        :return: sets sizer
        """
        self.sizer.Add(window=self.static_txt, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.sizer.Add(window=self.browser, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_LARGE)
        self.sizer.Add(window=self.submit_btn, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.SetSizer(self.sizer)
