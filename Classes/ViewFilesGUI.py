"""
Views the files of the client and lets the client choose which file to take
"""


from GeneralGUI import *


class ViewFilesGUI(GeneralGUI):
    """
    Views the files of the client and lets the client choose which file to take
    """
    def __init__(self, client, files, user_to_share):
        super().__init__(None, CHOOSE_FILE_TITLE, CHOOSE_USER_GUI_SIZE, client)
        self.btn_title = CHOOSE_FILE_BTN
        self.files = files
        self.user = user_to_share
        self.user_listbox = wx.ListBox(self.pnl, pos=wx.DefaultPosition, size=wx.DefaultSize, choices=self.get_files())
        self.choose_static = wx.StaticText(self.pnl, label=CHOOSE_USER_SHARE_STATIC)
        self.btn = wx.Button(self.pnl, label=self.btn_title)
        self.btn.Bind(wx.EVT_BUTTON, self.on_choose)
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

    def get_files(self):
        """
        :return: splits the string into a list
        """
        return self.files.split(FILE_SEPARATOR)

    def on_choose(self, e):
        """
        :param e: event handler
        :return: sends the choice to server
        """
        self.Close()
        file_choice = self.user_listbox.GetStringSelection()
        if file_choice != BLANK:
            message = self.client.username + SEPERATOR + ASK_FOR_FILE + SEPERATOR\
                      + self.user + SEPERATOR + file_choice
            self.client.send_request_to_server(self.client.my_socket, message)
            reply = self.client.read_server_response(self.client.my_socket)
