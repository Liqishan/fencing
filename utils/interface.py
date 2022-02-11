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
    def __init__(self, cfg: dict):
        super().__init__(daemon=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host, self.port = cfg['sendto']['ip'], cfg['sendto']['port']
        self.cfg = cfg
        messagedict = MessageDict(self.cfg)
        self.message = dict_to_json(messagedict.export())
        print(f'Send to {self.host}:{self.port} \n')

    def run(self) -> None:
        f = open('./log/fencing.log', 'a', encoding='utf8')
        while True:
            if self.message and isinstance(self.message, str):
                self.sock.sendto(self.message.encode(), (self.host, self.port))  # send to calculation module

                print(f'sent message: {self.message}')
                time.sleep(3)

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
