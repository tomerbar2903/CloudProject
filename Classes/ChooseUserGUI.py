"""
GUI window with a list box to choose a user to share / ask for share
"""


from GeneralGUI import *


class ChooseUserGUI(GeneralGUI):
    """
    list box a button
    """
    def __init__(self, title, btn_title, users):
        """
        :param title: ask for share \ share
        :param size: long and narrow
        """
        super().__init__(None, title, CHOOSE_USER_GUI_SIZE)
        self.user_listbox = wx.ListBox(self.pnl, pos=wx.DefaultPosition, size=wx.DefaultSize, choices=users)
        self.choose_static = wx.StaticText(self.pnl, label=CHOOSE_USER_SHARE_STATIC)
        self.btn = wx.Button(self.pnl, label=btn_title)
        self.btn_list_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.position()
        self.Show()

    def position(self):
        """
        :return: positions everything nicely
        """
        self.btn_list_sizer.Add(window=self.user_listbox, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_LARGE)
        self.btn_list_sizer.Add(window=self.btn, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_LARGE)
        self.txt_sizer.Add(window=self.choose_static, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_LARGE)
        self.sizer.Add(self.txt_sizer, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_LARGE)
        self.sizer.Add(self.btn_list_sizer, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_LARGE)
        self.SetSizer(self.sizer)
