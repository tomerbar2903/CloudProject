"""
The class for initiating the cloud path after sign up
"""


from ButtonFrame2 import *
from CONSTS import *
import subprocess


CLIENT_PROGRAM_PATH = R'E:\\12\\Project\\Classes\\Folder_Manager.py'


class InitCloudGUI(GeneralGUI):
    """
    creating the panel
    """
    def __init__(self):
        """
        initiating the panel
        """
        super().__init__(None, SELECT_DIRECTORY, INIT_CLOUD_GUI_SIZE)
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
        self.folder_manager.client.cloud = self.browser.GetPath()
        if self.folder_manager.client.cloud == BLANK:
            wx.MessageBox("You Must Choose A Folder To Continue!", 'Set-Up', wx.OK | wx.ICON_INFORMATION)
            self.Close()
            self.folder_manager.client.my_socket.close()
            InitCloudGUI()
        f = self.folder_manager.client.initiate_cloud()
        if not f:
            self.Close()
            self.folder_manager.client.my_socket.close()  # avoiding overflow
            InitCloudGUI()
        else:
            self.folder_manager.client.set_up()
            subprocess.run([PYTHON, CLIENT_PROGRAM_PATH, APP_MODE])
            wx.MessageBox("You Are All Set!", 'Set-Up', wx.OK | wx.ICON_INFORMATION)
            self.Close()

    def browse(self):
        """
        :return: the user can browse and select a folder
        """
        self.browser = wx.DirPickerCtrl()
        self.browser.Create(self.pnl, path="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                            style=wx.DIRP_DEFAULT_STYLE, name=wx.DirPickerCtrlNameStr)

    def order(self):
        """
        :return: sets sizer
        """
        self.sizer.Add(window=self.static_txt, proportion=0, flag=wx.ALL | wx.CENTER, border=7)
        self.sizer.Add(window=self.browser, proportion=0, flag=wx.ALL | wx.CENTER, border=12)
        self.sizer.Add(window=self.submit_btn, proportion=0, flag=wx.ALL | wx.CENTER, border=7)
        self.SetSizer(self.sizer)
