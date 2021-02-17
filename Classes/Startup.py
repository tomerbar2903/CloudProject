"""
gets startup directory
"""


from ReadRegistry import *
from CONSTS import *
import subprocess


class Startup(object):
    def __init__(self):
        """
        runs folder manager if registry is not empty
        """
        self.reg = ReadRegistry(CLIENT_REG)
        self.username = self.reg.read_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, USERNAME_REG)
        self.password = self.reg.read_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, PASSWORD_REG)
        if self.username != BLANK and self.password != BLANK:
            self.cloud = self.reg.read_registry(HKEY_LOCAL_MACHINE, CLIENT_REG, CLOUD_REG)
            self.run_client()

    def run_client(self):
        """
        :return: runs client in a thread
        """
        subprocess.run([PYTHON, self.cloud + PROJECT_FILES + "\\Folder_Manager.py", APP_MODE])


def main():
    """
    runs on startup
    """
    Startup()


if __name__ == '__main__':
    main()
