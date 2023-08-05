# -*- coding:utf-8 -*-
# @Time    : 2022/12/4 14:59
# @Author  : Ray Lam YL

import os
import os.path as osp
import re
import sys
from glob import glob
import shutil
import multiprocessing as mp

import cv2
import PIL.Image
import numpy as np


from rlylutils.image.utils import *
from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator
from rlylutils.files_op import Filesop

__all__ = ['Imgop']


@Decorator.cdec(Cfg.default['param'])
class Imgop(Filesop):

    default = {'src': 'image,nparray',    # 原始图像
               'center': 'center',  # 旋转中心，默认是[0,0]
               'scaler': 1,
               'rotate': 0,
               'delta_x': 0,
               'delta_y': 0
               }

    def __init__(self):
        self.__dict__.update(self.default)

    def __getitem__(self, f):
        ...

    def __str__(self, varname, iterable):
        return '【图片通用处理{}】len:{}'.format(varname, len(iterable))

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

    def read(self, f, resize_height=None, resize_width=None, normalization=False, colorSpace='BGR'):  # BGR
        """
        R
        :param f:
        :return:
        """
        img, rows, cols = read_image(f,
                                               resize_height=resize_height,
                                               resize_width=resize_width,
                                               normalization=normalization,
                                               colorSpace=colorSpace)

        return img, rows, cols

    def decode_read(self, f):
        """
        imread不支持中文路径，中文路径时用 R
        :param f: path
        :return: img ndarray
        """
        img = cv2.imdecode(np.fromfile(f, dtype=np.uint8), -1)
        rows = img.shape[0]
        cols = img.shape[1]
        return img, rows, cols

    def show(self, img):
        cv2.imshow('img', img)
        cv2.waitKey(0)
        #cv2.destroyAllWindows()

    def write(self, outpath, img):
        cv2.imwrite(outpath, img)
