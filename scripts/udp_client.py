# coding=utf-8

# author: Reggie
# time:   2019/08/21 13:45

import socket


def udp_client():
    # 创建socket对象
    # SOCK_DGRAM    udp模式
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # 发送数据 字节
    host = "<broadcast>"
    s.sendto("你好".encode(), (host, 8000))


if __name__ == '__main__':
    udp_client()

