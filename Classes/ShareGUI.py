"""
The window where you share yourself
"""


from ChooseUserGUI import *
from GeneralGUI import *
import os


class ShareGUI(GeneralGUI):
    """
    opens a window with directory dialog and a Next button
    """
    def __init__(self, client):
        """
        :param e: event handler
        """
        super().__init__(None, SHARE_TITLE, INIT_CLOUD_GUI_SIZE, client)
        self.file_to_share = None
        self.static_txt = wx.StaticText(self.pnl, label=CHOOSE_FILE_TO_SHARE)
        self.next_btn = wx.Button(self.pnl, label=NEXT_BTN)
        self.next_btn.Bind(wx.EVT_BUTTON, self.on_next)
        self.browser = wx.FilePickerCtrl()
        self.browser.Create(self.pnl, path=self.client.cloud, pos=wx.DefaultPosition, size=wx.DefaultSize,
                            style=wx.DIRP_DEFAULT_STYLE, name=wx.DirPickerCtrlNameStr)
        self.position()
        self.Show()

    def position(self):
        """
        :return: positions everything nicely
        """
        self.sizer.Add(window=self.static_txt, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.sizer.Add(window=self.browser, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_LARGE)
        self.sizer.Add(window=self.next_btn, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.SetSizer(self.sizer)

    def on_next(self, e):
        """
        :param e: event handler
        :return: opening new window after checking that the file is in the cloud
        """
        self.file_to_share = self.browser.GetPath()
        check = (self.client.cloud in self.file_to_share and os.path.isfile(self.file_to_share))  # checks if file in cloud
        if not check:
            wx.MessageBox("You Must Choose A File In Your Cloud Folder", 'Share', wx.OK | wx.ICON_INFORMATION)
            self.Close()
            ShareGUI(self.client)
        else:
            self.Close()
            ChooseUserGUI(CHOOSE_USER_SHARE_STATIC, SHARE_BTN, [self.file_to_share], self.client)
