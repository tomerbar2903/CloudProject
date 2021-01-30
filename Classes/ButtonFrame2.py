"""
GUI Frame of logging in or signing up
"""

from GeneralGUI import *
from CONSTS import *


class ButtonFrame2(GeneralGUI):
    def __init__(self, e, frame_title, static_txt, b1_title, b2_title, size, client):
        """
        initiates frame
        """
        super().__init__(e, frame_title, size, client)
        self.t1 = wx.StaticText(self.pnl, label=static_txt)
        self.btn1, self.btn2 = self.init_buttons(b1_title, b2_title)
        self.h_sizer = wx.BoxSizer()
        self.positions()
        self.Show()

    def positions(self):
        """
        :return: puts to positions
        """
        self.sizer.Add(window=self.t1, proportion=PROPORTION,
                       flag=wx.ALL | wx.CENTER, border=BORDER_LARGE)
        self.sizer.Add(window=self.btn1, proportion=PROPORTION,
                       flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.sizer.Add(window=self.btn2, proportion=PROPORTION,
                       flag=wx.ALL | wx.CENTER, border=BORDER_SMALL)
        self.SetSizer(self.h_sizer)
        self.SetSizer(self.sizer)

    def init_buttons(self, b1_title, b2_title):
        """
        :param b1_title: label of button 1
        :param b2_title: label of button 2
        :return: the buttons
        """
        btn1 = wx.Button(self.pnl, label=b1_title)
        btn2 = wx.Button(self.pnl, label=b2_title)
        return btn1, btn2
