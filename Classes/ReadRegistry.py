"""
reads and writes registry
"""

from winreg import *
from CONSTS import *


VALUES_COUNT = 3
CLIENT_COUNT = 2
BIG_NUMBER = 1000
CLIENT_PATH = r"SOFTWARE\WOW6432Node\Cloud Server\Client"
SERVER_PATH = r"SOFTWARE\WOW6432Node\Drive Server"
NAME = "CLOUD_PATH"


class ReadRegistry(object):
    def __init__(self, reg_path):
        """
        initiates registry
        """
        try:
            self.raw_key = OpenKey(HKEY_LOCAL_MACHINE, reg_path)
        except Exception as msg:
            print("error at ReadRegistry constructor", msg)

    def get_ip_port(self):
        """
        :return: reads the ip and port from registry
        """
        ip = BLANK
        port = BLANK
        for i in range(VALUES_COUNT):
            try:
                name, value, typ = EnumValue(self.raw_key, i)
                if name == IP_REG:
                    ip = value
                if name == PORT_REG:
                    port = value
            except EnvironmentError:
                print("You have ", i, " values")
                break
        CloseKey(self.raw_key)
        return ip, port

    def get_cloud(self):
        """
        :return: cloud path for server
        """
        for i in range(VALUES_COUNT):
            try:
                name, value, typ = EnumValue(self.raw_key, i)
                if name == NAME:
                    return value
            except EnvironmentError:
                print("You have ", i, " values")
                break
        CloseKey(self.raw_key)
        return ""

    def read_client_cloud(self):
        """
        :return: cloud path for client
        """
        for i in range(CLIENT_COUNT):
            try:
                name, value, typ = EnumValue(self.raw_key, i)
                if name == CLOUD_REG:
                    return value
            except EnvironmentError:
                break
        CloseKey(self.raw_key)
        return ""

    @staticmethod
    def set_client_cloud(cloud):
        """
        :param cloud: the entered cloud
        :return: -
        """
        try:
            write_key = OpenKey(HKEY_LOCAL_MACHINE, CLIENT_REG, REG_CONST, KEY_WRITE)
            SetValueEx(write_key, NAME, REG_CONST, REG_SZ, cloud)
            CloseKey(write_key)
        except WindowsError as msg:
            print("at set_client_cloud", msg)

    @staticmethod
    def read_registry(department, reg_path, value_name):
        """
        :param reg_path: path to key
        :param value_name: key
        :return: the key's value
        """
        key = OpenKey(department, reg_path, REG_CONST, KEY_READ)
        for i in range(BIG_NUMBER):
            try:
                name, value, typ = EnumValue(key, i)
                if name == value_name:
                    return value
            except EnvironmentError:
                break
        CloseKey(key)
        return BLANK

    @staticmethod
    def set_registry(department, reg_path, value_name, value):
        """
        :param reg_path: path to key
        :param value_name: key's name
        :param value: the new value
        :return: -
        """
        write_key = OpenKey(department, reg_path, REG_CONST, KEY_WRITE)
        SetValueEx(write_key, value_name, REG_CONST, REG_SZ, value)
        CloseKey(write_key)

    @staticmethod
    def set_observer(value):
        """
        :param value: Deny \ Allow
        :return: changes the value
        """
        write_key = OpenKey(HKEY_LOCAL_MACHINE, CLIENT_REG, REG_CONST, KEY_WRITE)
        SetValueEx(write_key, OBSERVER, REG_CONST, REG_SZ, value)
        CloseKey(write_key)
