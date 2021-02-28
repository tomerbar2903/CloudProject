"""
gets startup directory
"""


from ReadRegistry import *
from CONSTS import *
import subprocess
import getpass


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

    @staticmethod
    def run_client():
        """
        :return: runs client in a thread
        """
        path_to_program = PATH_TO_PROJECT_FILES % getpass.getuser() + "\\Programs\\Folder_Manager.py"
        subprocess.run([PYTHON, path_to_program, APP_MODE])


def main():
    """
    runs on startup
    """
    Startup()


if __name__ == '__main__':
    main()
