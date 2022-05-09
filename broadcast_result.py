# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/5/9 14:10

import abc

from version import VERSION


class ResultNotFoundError(Exception):
    pass


class BaseResult(object):
    @abc.abstractmethod
    def to_dict(self, *args, **kwargs):
        return NotImplemented


class Result(BaseResult):
    def __init__(self, action, code, params, message, data):
        self.action = action
        self.code = code
        self.params = params
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "action": self.action,
            "params": self.params,
            "code": self.code,
            "data": self.data,
            "message": self.message
        }

    @property
    def dict(self):
        return self.to_dict()

    def __repr__(self):
        result = ""
        dict_info = self.to_dict()
        keys = sorted(dict_info.keys(), key=lambda x: x)
        for k in keys:
            result += "%s:\t%s\n" % (k, dict_info[k])
        return result


version_result = {
    VERSION: Result
}


def result(*args, version=VERSION, **kwargs):
    try:
        return version_result[version](*args, **kwargs)
    except KeyError:
        raise ResultNotFoundError("version result not found")

