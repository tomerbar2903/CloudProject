"""
changes the registry 'folder_manager' value to be no
"""


from ReadRegistry import *


class OnShutdown(object):
    def __init__(self):
        """
        sets the folder_manger value to be no - so that on startup it will go on
        """
        self.reg = ReadRegistry()
        self.reg.set_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, FOLDER_MANAGER_REG, NO_REG)


def main():
    """
    sets the registry
    """
    OnShutdown()


if __name__ == '__main__':
    main()
