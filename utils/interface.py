# Time      :9/23/21 12:01 PM
# Author    :siyangxie
# File      :main.py
# Email     :xiesiyang@126.com

import json
import socket
import time
from threading import Thread

# import mysql.connector


class Sender(Thread):
    """
    Sender thread. Currently we just use the cfg file.
    """
    def __init__(self, host: str, port: int, cfg: dict):
        super().__init__(daemon=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.cfg = cfg

        # ip, username, password, database, table = self.cfg['mysql']
        # self.db = DBConnector(user=username, password=password, host=self.cfg['mysql'][0], database=database,
        #                       camera_ip=self.cam_ip, cfg=self.cfg)  # db initialization
        # self.message = self.generate_message_str()  # read first time
        messagedict = MessageDict(self.cfg)
        self.message = dict_to_json(messagedict.export())

    def run(self) -> None:
        f = open('./fencing.log', 'a', encoding='utf8')
        while True:
            if self.message and isinstance(self.message, str):
                self.sock.sendto(self.message.encode(), (self.host, self.port))  # send to calculation module
                # print debug info in log file
                # f.write(f'sent message: {self.message}'+'\n')
                print(f'sent message: {self.message}')
                time.sleep(3)


    # def generate_message_str(self) -> str:
    #     ip, area = self.db.read()  # read from mysql
    #     return dict_to_json({'protocol_id': 102, 'detected': True, 'area': area})  # convert area coords to json message


# class DBConnector:
#     """
#     MySQL connector. Used in Sender thread.
#     """
#     def __init__(self, user, password, host, database, camera_ip, cfg):
#         self.user = user
#         self.password = password
#         self.host = host
#         self.database = database
#         self.camera_ip = camera_ip
#         self.cfg = cfg
#
#         self.cnx = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
#         self.cursor = self.cnx.cursor(buffered=True)
#         self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')
#         self.cursor.execute('SHOW DATABASES')
#
#         print('\ndatabases...')
#         for i in self.cursor:
#             print(i)
#         print('\n')
#
#         self.connect()
#         self.cursor.execute(f'CREATE TABLE IF NOT EXISTS virfen '
#                             f'(camera_ip VARCHAR(64), area VARCHAR(128), primary key (camera_ip))')
#         self.disconnect()
#         self.init(area=cfg['area'])
#
#     def insert(self, area: list) -> None:
#         """
#         For testing purposes only. Not used in production.
#         :param area:
#         :return:
#         """
#         self.connect()
#         area = area.__str__()
#         self.cursor.execute('INSERT INTO virfen (camera_ip, area) VALUES (%s, %s) ON DUPLICATE KEY UPDATE area = %s',
#                             (self.camera_ip, area, area))
#         self.cnx.commit()
#         self.disconnect()
#
#     def init(self, area: list) -> None:
#         """
#         Everytime after reboot, we need to check MySQL. If row exists, we read it. If not, we read from fen-config.yaml,
#         and commit it to MySQL as default setup.
#         :param area:
#         :return:
#         """
#         self.connect()
#         self.cursor.execute('SELECT * from virfen WHERE camera_ip = %s', (self.camera_ip,))
#         data = self.cursor.fetchone()
#
#         if not data:
#             area = area.__str__()
#             self.cursor.execute(
#                 'INSERT INTO virfen (camera_ip, area) VALUES (%s, %s) ON DUPLICATE KEY UPDATE area = %s',
#                 (self.camera_ip, area, area))
#             self.cnx.commit()
#
#         self.disconnect()
#
#     def read(self) -> tuple:
#         """
#         Read from MySQL.
#         :return: a tuple of (camera_ip, area), e.g. ('192.168.0.89', '[[1,2,3,4],[5,6,7,8],[9,0,1,2],[3,4,5,6]]')
#         """
#         self.connect()
#         self.cursor.execute('SELECT * from virfen WHERE camera_ip = %s', (self.camera_ip,))
#         res = self.cursor.fetchone()
#         self.disconnect()
#         return res
#
#     def disconnect(self) -> None:
#         """
#         General disconnection to MySQL.
#         :return:
#         """
#         self.cursor.close()
#         self.cnx.close()
#
#     def connect(self) -> None:
#         """
#         General connection to MySQL.
#         :return:
#         """
#         self.cnx = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
#                                            database=self.database)
#         self.cursor = self.cnx.cursor(buffered=True)
#
#
# class Listener(Thread):
#     def __init__(self, port: int):
#         super().__init__()
#         self.port = port
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
#     def run(self) -> None:

class MessageDict:
    def __init__(self, cfg):
        self.protocol_id = 102
        self.detected = 1
        self.front, self.rear = cfg['front'], cfg['rear']

    def export(self):
        res = self.__dict__.copy()
        return res


def dict_to_json(message: dict) -> str:
    """
    Convert dict to json.
    :param message:
    :return:
    """
    return json.dumps(message)


def json_to_dict(message: str) -> dict:
    """
    Convert json to dict.
    :param message:
    :return:
    """
    return json.loads(message)
