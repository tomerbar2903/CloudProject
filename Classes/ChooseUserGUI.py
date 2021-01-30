"""
GUI window with a list box to choose a user to share / ask for share
"""


from GeneralGUI import *
from ReadRegistry import *


class ChooseUserGUI(GeneralGUI):
    """
    list box a button
    """
    def __init__(self, title, btn_title, args, client):
        """
        :param title: ask for share \ share
        :param size: long and narrow
        """
        super().__init__(None, title, CHOOSE_USER_GUI_SIZE, client)
        self.args = args  # arguments
        self.title = title  # saves it for later use
        self.btn_title = btn_title  # saves it for later use
        self.mode = SHARE_MODE
        if btn_title == ASK_FOR_SHARE_BTN:
            self.mode = ASK_FOR_SHARE_MODE
        self.users = self.get_users()
        self.user_listbox = wx.ListBox(self.pnl, pos=wx.DefaultPosition, size=wx.DefaultSize, choices=self.users)
        self.choose_static = wx.StaticText(self.pnl, label=CHOOSE_USER_SHARE_STATIC)
        self.btn = wx.Button(self.pnl, label=btn_title)
        self.btn.Bind(wx.EVT_BUTTON, self.on_share)
        self.btn_list_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.position()
        self.Show()

    def position(self):
        """
        :return: positions everything nicely
        """
        self.btn_list_sizer.Add(window=self.user_listbox, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.btn_list_sizer.Add(window=self.btn, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.txt_sizer.Add(window=self.choose_static, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.sizer.Add(self.txt_sizer, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.sizer.Add(self.btn_list_sizer, proportion=PROPORTION, flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.SetSizer(self.sizer)

    def get_users(self):
        """
        :return: list of users minus current one
        """
        message = self.client.username + SEPERATOR + GET_USERS
        self.client.send_request_to_server(self.client.my_socket, message)
        users = self.client.read_server_response(self.client.my_socket).decode().split(
            SEPERATOR)
        return users

    def on_share(self):
        """
        :return: sends server a message according to mode
        """
        user_to_share = self.user_listbox.GetStringSelection()
        if self.mode == SHARE_MODE:
            message = self.client.username + SEPERATOR + SHARE + SEPERATOR + user_to_share + \
                      SEPERATOR + self.args[START]
            self.client.send_request_to_server(message)
            reply = self.client.read_server_response(self.client.my_socket)
            if reply == MESSAGE_SENT:
                message_txt = "File Shared With %s" % user_to_share
                wx.MessageBox(message_txt, 'Share', wx.OK | wx.ICON_INFORMATION)
            else:
                message_txt = "Error At Sharing With %s" % user_to_share
                wx.MessageBox(message_txt, 'Share', wx.OK | wx.ICON_INFORMATION)
                self.Close()
                ChooseUserGUI(self.title, self.btn_title, self.mode, self.client)
