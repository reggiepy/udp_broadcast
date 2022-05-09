# coding=utf-8

# author: Reggie
# time:   2019/08/21 14:29

import argparse
import pickle
import socket
import sys

from utils import From, get_all_address


def filter_ipv4_broadcast(ipv4_address):
    return From(ipv4_address) \
        .filter(lambda x: x != "127.0.0.1") \
        .map(lambda x: x.rpartition(".")) \
        .map(lambda x: x[0] + ".255") \
        .to_order_set_list()


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
    print("action:%s%s" % ("\t" * 3, args.action))
    print("cmd:%s%s" % ("\t" * 3, args.cmd))
    print("host:%s%s" % ("\t" * 3, args.host))

    if args.host:
        ipv4_broadcasts = filter_ipv4_broadcast(args.host.split(","))
    else:
        ipv4_broadcasts = filter_ipv4_broadcast(get_all_address())
    print("broadcast:%s%s" % ("\t" * 2, ", ".join(ipv4_broadcasts)))
    if not ipv4_broadcasts:
        print("please input one of ipv4 host")
        exit(1)
    print()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(5)
    PORT = 1060

    # network = '<broadcast>'
    # network = '192.168.1.255'
    for network in ipv4_broadcasts:
        print(network.center(50, "-"))
        print("action:%s%s" % ("\t" * 2, args.action))
        print("cmd:%s%s" % ("\t" * 2, args.cmd))
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
            result = pickle.loads(rec)
            print("data:%s%s" % ("\t" * 2, result.data))
