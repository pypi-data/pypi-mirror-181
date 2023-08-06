# -*- coding:utf-8 -*-
# @Time    : 2022/12/7 17:08
# @Author  : Ray Lam YL

from moviepy.editor import *

from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator

__all__ = ['Vieop']


@Decorator.cdec(Cfg.default['param'])
class Vieop:

    default = {
               }

    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【视频通用处理{}】len:{}'.format(varname, len(iterable))

    @classmethod
    def add_params(cls, **kwargs):
        cls.default.update(**kwargs)

    def process(self):
        ...

    def namestr(self, obj, namespace):
        """
        变量名转字符串
        #例（变量名，globals()）
        :param obj:
        :param namespace:
        :return:
        """

        return [name for name in namespace if namespace[name] is obj][0]

    def multiprocess(self):
        """
        #多进程
        :return:
        """
        ...