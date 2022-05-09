# coding=utf-8

# author: Reggie
# time:   2019/08/21 13:57


import json
import math
import random
import socket

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT = 9999
hostname = socket.gethostname()
machineName = socket.getfqdn(hostname)
machineAddress = socket.gethostbyname(machineName)

message = {
    "ip": machineAddress,
    "hostname": hostname,
    "machineName": machineName,
    "random": math.floor(random.random() * 10000)
}

network = '<broadcast>'
sender.sendto(json.dumps(message).encode('utf-8'), (network, PORT))
