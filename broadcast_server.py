# coding=utf-8

# author: Reggie
# time:   2019/08/21 14:29

# -*- coding:utf-8 -*-

import os
import pickle
import socket

from broadcast_result import result


def cmd(cmd):
    p = os.popen(cmd, 'r', 1)
    dat = p.read()
    p.close()
    return dat


def get_result(action, code, params, message, data):
    return {
        "action": action,
        "params": params,
        "code": code,
        "data": data,
        "message": message
    }


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    PORT = 1060
    s.bind(('', PORT))
    print('Listen...', s.getsockname())

    while True:
        data, address = s.recvfrom(65535)
        rec = pickle.loads(data)
        print('<-{}:{}'.format(address, rec))
        sent = ""
        res = ""
        if rec['action'] == "cmd":
            if not rec["params"]:
                continue
            if rec["params"]:
                res = cmd(rec['params'])
            sent = pickle.dumps(result("cmd", 0, rec['params'], "操作成功", res))
            print('-> {}'.format(address))
        s.sendto(sent, address)


if __name__ == '__main__':
    main()
