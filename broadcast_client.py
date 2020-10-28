# coding=utf-8

# author: Reggie
# time:   2019/08/21 14:29

import socket
import pickle
import argparse
import time

class From:
    def __init__(self, src):
        self.src = src

    def toList(self):
        return list(self.src)

    def toOrderSetList(self, reverse=False):
        tmp = self.toList()
        return sorted(set(tmp), key=tmp.index, reverse=reverse)

    def map(self, func):
        return From(map(func, self.src))

    def filter(self, predicate):
        return From(filter(predicate, self.src))


def get_ipv4_broadcasts():
    hostname = socket.gethostname()
    # family: AF_INET ipv4、AF_INET6 ipv6, None 为所有
    addrs = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    ipv4_broadcasts = From(addrs) \
        .map(lambda x: x[4][0].rpartition(".")) \
        .map(lambda x: x[0] + ".255") \
        .toOrderSetList()
    return ipv4_broadcasts


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', help='the action you want to send', default="cmd")
    parser.add_argument('-c', '--cmd', help='the command you want to execute')
    args = parser.parse_args()
    print(args.action, args.cmd)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(5)
    PORT = 1060

    ipv4_broadcasts = get_ipv4_broadcasts()
    print(ipv4_broadcasts)
    # network = '<broadcast>'
    # network = '192.168.1.255'
    for network in ipv4_broadcasts:
        sent_data = {
            'action': args.action,
            'params': args.cmd
        }
        s.sendto(pickle.dumps(sent_data), (network, PORT))
        try:
            rec = s.recv(65535)
        except Exception as _:
            pass
        else:
            b = pickle.loads(rec)
            print(network.center(50, "-"))
            msg = "action:\t\t{}\ncmd:\t\t{}\ndata:\n{}"\
                .format(args.action, args.cmd, b['data']['result'])
            print(msg)
