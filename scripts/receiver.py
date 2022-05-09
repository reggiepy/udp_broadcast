# coding=utf-8

# author: Reggie
# time:   2019/08/21 13:57

import socket

socketReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketReceiver.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT = 9999

socketReceiver.bind(('', PORT))
print('Listening for broadcast at ', socketReceiver.getsockname())

while True:
    data, address = socketReceiver.recvfrom(65535)
    print('Server received from {}:{}'.format(address, data.decode('utf-8')))

