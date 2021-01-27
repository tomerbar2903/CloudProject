"""
makes exe file - comfort file
"""


import subprocess


FILE_PATH = R"E:\12\Project\Classes\pyinstaller_command.txt"


def main():
    """
    add your shit here
    """
    command = open(FILE_PATH, 'r')
    subprocess.run(command.read())


if __name__ == '__main__':
    main()
