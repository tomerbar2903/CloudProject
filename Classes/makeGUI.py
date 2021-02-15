"""
make GUI exe
"""


import subprocess


COMMAND = r"pyinstaller E:\12\Project\Classes\GUI_exe.py --noconfirm --onedir --windowed --icon " \
          r"E:/12/Project/cloud_icon(1).ico --add-data E:\12\Project\Classes\ReadRegistry.py " \
          r" E:/12/Project/Classes/File.py;. E:/12/Project/Classes/ShareGUI.py;. " \
          r"E:/12/Project/Classes/SystemRegisterGUI.py;. E:/12/Project/Classes/ButtonFrame2.py;." \
          r" E:/12/Project/Classes/RegisterPanel.py;."


def main():
    """
    makes exe
    """
    subprocess.run(COMMAND)


if __name__ == '__main__':
    main()
