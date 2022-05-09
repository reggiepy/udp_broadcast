# coding=utf-8

# author: Reggie
# time:   2019/08/21 14:29

# -*- coding:utf-8 -*-

import os
import pickle
import socket

import version


def cmd(cmd):
    p = os.popen(cmd, 'r', 1)
    dat = p.read()
    p.close()
    return dat


def get_result(action, code, params, message, dat):
    r = {
        "version": version.VERSION,
        "action": action,
        "params": params,
        "code": code,
        "data": dat,
        "message": message
    }
    return r


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
        if rec['action'] == "cmd":
            if not rec["params"]:
                print("no params specified")
                continue
            res = cmd(rec['params'])
            sent = pickle.dumps(get_result("cmd", 0, rec['params'], "操作成功", {'result': res}))
            print('-> {}'.format(address))
        s.sendto(sent, address)


if __name__ == '__main__':
    main()
