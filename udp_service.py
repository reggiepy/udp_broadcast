# coding=utf-8

# author: Reggie
# time:   2019/08/21 13:45

import threading
import socket


def udp_service():
    # 创建socket对象
    # SOCK_DGRAM    udp模式
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", 8000))  # 绑定服务器的ip和端口
    print(s.getsockname())
    while True:
        # data = s.recv(1024)  # 一次接收1024字节
        data, ip = s.recvfrom(1024)  # 一次接收1024字节
        print(data.decode(), ip)  # decode()解码收到的字节
    # 不需要建立连接


if __name__ == '__main__':
    udp_service()


