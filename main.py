# Time      :9/23/21 12:01 PM
# Author    :siyangxie
# File      :main.py
# Email     :xiesiyang@126.com


import argparse

import yaml

from utils import interface


def run():
    sender = interface.Sender(host=opt.host, port=opt.port, cfg=cfg)
    sender.run()

    while True:
        pass


if __name__ == '__main__':
    cfg = yaml.load(open('config/fen-config.yaml'), Loader=yaml.FullLoader)
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1', help='calculation host')
    parser.add_argument('--port', type=int, default=25542, help='calculation port')
    opt = parser.parse_args()
    print(opt)

    run()
