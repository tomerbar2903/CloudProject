"""
Class File - contains properties:
1. name
2. path
3. format
TOMER BAR 16/09/2020
"""
from CONSTS import *
import os


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
        self.path = self.path.split(DOT)[START] + DOT + self.format

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

    def set_name(self, name):
        """
        :param name: new name of file
        :return: -
        """
        self.name = name
        self.path = self.get_directory() + "\\" + self.name + DOT + self.format

    @staticmethod
    def validate_file(file_path):
        """
        :param file_path: the directory to check no duplicate names
               i: int that holds the number of the new file
        :return: the file name or the file name(1)
        """
        i = ADDER
        file_obj = File(file_path)
        folder = file_obj.get_directory()
        file_list = os.listdir(folder)
        real_file_list = []
        for file in file_list:
            if DOT in file and File(file).format == CLOUD_FORMAT:
                real_file_list.append(File(file).name)
        file_name = file_obj.name
        if file_name not in real_file_list:  # if the name doesn't exist
            return file_path
        # checks for (i)
        done = False
        while not done:
            if file_name + " (" + str(i) + ")" in real_file_list:
                i += ADDER
            else:
                file_name = file_name + " (" + str(i) + ")"
                done = True
        file_obj.set_name(file_name)
        os.rename(file_path, file_obj.path)
        return file_obj.path

    def get_directory(self):
        """
        :return: the directory to the file
        """
        return "\\".join(self.path.split("\\")[:END])

    def new_format_path(self, format):
        """
        :param format: the new format
        :return: the same path but with new format
        """
        path_format = self.path.split('.')
        path_format[SECOND] = format
        return ".".join(path_format)

