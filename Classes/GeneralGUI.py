"""
The GUI version of Folder Manager
"""

import wx
from CONSTS import *
from Folder_Manager import MyHandler


ICON_PATH = r"E:\12\Project\cloud_icon (1).ico"


class GeneralGUI(wx.Frame):
    def __init__(self, e, title, size, client):
        """
        initiates the app
        """
        super().__init__(e, title=title, size=size)
        # CREATING PANEL
        self.client = client
        self.pnl = self.panel()
        self.InitUI()
        icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

    def InitUI(self):
        """
        :return: initiates all properties of the frame (GUI)
        """
        try:
            # creates menu bar
            menu_bar = wx.MenuBar()

            # creates menu
            file_menu = wx.Menu()

            # once the item is clicked, the menu closes
            menu_item = file_menu.Append(wx.ID_EXIT,
                                         QUIT_BTN, QUIT_APP)

            # initiates 'Menu' as the name
            menu_bar.Append(file_menu, MENU_GUI)

            # sets menu bar
            self.SetMenuBar(menu_bar)

            # binds on_quit method to Quit button
            self.Bind(wx.EVT_MENU, self.on_quit, menu_item)

            self.Center()
        except Exception as msg:
            print("error on GUI_class, InitUI:", msg)

    def panel(self):
        """
        :return: initiating panel
        """
        try:
            # initiating panel
            pnl = wx.Panel(self)
            return pnl
        except Exception as msg:
            print("at panel:", msg)

    def on_quit(self, e):
        """
        :param e: event of close
        :return: close the window
        """
        self.client.end()
        self.Close()

