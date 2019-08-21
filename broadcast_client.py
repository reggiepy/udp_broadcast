# coding=utf-8

# author: Reggie
# time:   2019/08/21 14:29

import socket
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--action', help='the action you want to send')
parser.add_argument('-c', '--cmd', help='the command you want to execute')
args = parser.parse_args()

print(args.action, args.cmd)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT = 1060

network = '<broadcast>'
sent_data = {
    'action': args.action,
    'params': args.cmd
}
s.sendto(pickle.dumps(sent_data), (network, PORT))
rec = s.recv(65535)
b = pickle.loads(rec)
print("data:", b['data']['result'])
