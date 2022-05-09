# coding=utf-8

# author: Reggie
# time:   2019/08/21 14:29

import argparse
import pickle
import socket
import sys


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


def gen_ipv4_broadcast(ipv4_address):
    return From(ipv4_address) \
        .map(lambda x: x.rpartition(".")) \
        .map(lambda x: x[0] + ".255") \
        .toOrderSetList()


def get_ipv4_broadcasts():
    hostname = socket.gethostname()
    # family: AF_INET ipv4、AF_INET6 ipv6, None 为所有
    addrlist = socket.getaddrinfo(hostname, None, family=socket.AF_INET)
    ipv4_address = From(addrlist).map(lambda x: x[4][0]).toOrderSetList()
    return gen_ipv4_broadcast(ipv4_address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--action',
        help='the action you want to send',
        default="cmd"
    )
    parser.add_argument(
        '-c',
        '--cmd',
        help='the command you want to execute'
    )
    parser.add_argument(
        '--host',
        help='the host to broadcast, same as --host 127.0.0.1,192.168.1.1 use "," to split',
        default=""
    )
    args = parser.parse_args()
    print(args.action, args.cmd, args.host)

    if args.host:
        ipv4_broadcasts = gen_ipv4_broadcast(args.host.split(","))
    else:
        ipv4_broadcasts = get_ipv4_broadcasts()
    print(ipv4_broadcasts)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(5)
    PORT = 1060

    # network = '<broadcast>'
    # network = '192.168.1.255'
    for network in ipv4_broadcasts:
        print(network.center(50, "-"))
        print("action:\t\t%s" % args.action)
        print("cmd:\t\t%s" % args.cmd)
        sent_data = {
            'action': args.action,
            'params': args.cmd
        }
        try:
            s.sendto(pickle.dumps(sent_data), (network, PORT))
            rec = s.recv(65535)
        except Exception as e:
            print("socket error: %s exc_info: %s" % (e, sys.exc_info()))
        else:
            b = pickle.loads(rec)
            data = b['data']['result']
            print("data:\t\t%s" % data)
