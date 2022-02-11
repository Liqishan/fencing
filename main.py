# Time      :9/23/21 12:01 PM
# Author    :siyangxie
# File      :main.py
# Email     :xiesiyang@126.com


import argparse

import yaml

from utils import interface


def run():
    sender = interface.Sender(cfg=cfg)
    sender.run()
    while True:
        pass

if __name__ == '__main__':
    cfg = yaml.load(open('config/fen-config.yaml'), Loader=yaml.FullLoader)
    run()
