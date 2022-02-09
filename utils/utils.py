# Time      :9/23/21 12:01 PM
# Author    :siyangxie
# File      :main.py
# Email     :xiesiyang@126.com


import re


def extract_ip_port(source: str) -> list:
    """
    :param source: 'rtsp://admin:wingo123456@192.168.2.51:554/h264/ch1/main/av_stream'
    :return: ['192.168.2.51':'554']
    """
    return re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', source)[0].split(':')
