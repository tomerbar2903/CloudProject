"""
GUI window with a list box to choose a user to share / ask for share
"""


from ViewFilesGUI import *


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
        self.args = args  # arguments - empty list of file to share
        self.title = title  # saves it for later use
        self.btn_title = btn_title  # saves it for later use
        self.mode = SHARE_MODE
        if btn_title == ASK_FOR_SHARE_BTN:
            self.mode = ASK_FOR_SHARE_MODE
        self.users = self.get_users()
        self.user_listbox = wx.ListBox(self.pnl, pos=wx.DefaultPosition, size=wx.DefaultSize, choices=self.users)
        if self.mode == SHARE_MODE:
            self.choose_static = wx.StaticText(self.pnl, label=CHOOSE_USER_SHARE_STATIC)
        elif self.mode == ASK_FOR_SHARE_MODE:
            self.choose_static = wx.StaticText(self.pnl, label=CHOOSE_USER_SHARE_TITLE)
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
        if self.mode == SHARE_MODE:
            message = self.client.username + SEPERATOR + GET_USERS
            self.client.send_request_to_server(self.client.my_socket, message)
            users = self.client.read_server_response(self.client.my_socket).decode().split(
                SEPERATOR)
        elif self.mode == ASK_FOR_SHARE_MODE:
            message = self.client.username + SEPERATOR + GET_ONLINE_USERS
            self.client.send_request_to_server(self.client.my_socket, message)
            users = self.client.read_server_response(self.client.my_socket).decode()
            if users != NO_ONLINE:
                return users.split(SEPERATOR)
            else:
                return []
        return users

    def on_share(self, e):
        """
        :return: sends server a message according to mode
        """
        self.Close()
        user_to_share = self.user_listbox.GetStringSelection()
        if user_to_share != BLANK:
            if self.mode == SHARE_MODE:
                message = self.client.username + SEPERATOR + SHARE + SEPERATOR + user_to_share + \
                          SEPERATOR + self.client.without_cloud(self.args[START])
                self.client.send_request_to_server(self.client.my_socket, message)
                reply = self.client.read_server_response(self.client.my_socket)
                if reply.decode() == MESSAGE_SENT:
                    message_txt = "Your Message To %s Was Sent" % user_to_share
                    wx.MessageBox(message_txt, 'Share', wx.OK | wx.ICON_INFORMATION)
                    self.Close()
                elif reply.decode() == REQUEST_EXISTS:
                    message_txt = "You Sent This File To %s In The Past" % user_to_share
                    wx.MessageBox(message_txt, 'Share', wx.OK | wx.ICON_INFORMATION)
                    self.Close()
                    ChooseUserGUI(self.title, self.btn_title, self.mode, self.client)
            elif self.mode == ASK_FOR_SHARE_MODE:
                message = self.client.username + SEPERATOR + ASK_FOR_SHARE + SEPERATOR + user_to_share
                self.client.send_request_to_server(self.client.my_socket, message)
                files = self.client.read_server_response(self.client.my_socket).decode()
                if files != NO_FILES:
                    ViewFilesGUI(self.client, files, user_to_share)
                else:
                    message_txt = "%s Has No Files Yet" % user_to_share
                    wx.MessageBox(message_txt, 'Share', wx.OK | wx.ICON_INFORMATION)
        else:
            ChooseUserGUI(self.title, self.btn_title, self.mode, self.client)

