"""
Class File - contains properties:
1. name
2. path
3. format
TOMER BAR 16/09/2020
"""
from CONSTS import *


END = -1
START = 0


class File(object):
    """
    the class of File
    """
    def __init__(self, path):
        """
        definition of file
        """
        self.path = path
        self.name = self.get_name()
        self.format = self.get_format()

    def get_name(self):
        """
        :return: returns the name of the file
        """
        file_props = self.path.split('\\')
        file_name = file_props[END].split('.')[START]
        return file_name

    def get_format(self):
        """
        :return: the file's format
        """
        file_props = self.path.split('\\')
        file_format = file_props[END].split('.')[END]
        return file_format

    def set_format(self, format):
        """
        changes format of current file
        :return: -
        """
        self.format = format

    def change_file_to_cloud(self, cloud_format):
        """
        changes the file's path to cloud formatted one
        :return: the new path
        """
        directory = self.path.split('\\')[:END]
        directory = '\\'.join(directory)
        return directory + '\\' + self.name + '.' + cloud_format

    def make_new_file_path(self, folder):
        """
        :param new_path: new path of file to merge
        :return: the new path
        """
        return folder + '\\' + self.name + '.' + self.format

    def new_format_path(self, format):
        """
        :param format: the new format
        :return: the same path but with new format
        """
        path_format = self.path.split('.')
        path_format[SECOND] = format
        return ".".join(path_format)
