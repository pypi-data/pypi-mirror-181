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

    def letterbox_image(self, image):
        """
        图片统一尺寸，补灰条操作
        :param: image
        :return: new_image
        """
        ih = image.shape[0]
        iw = image.shape[1]

        w = self.width
        h = self.height

        scale = min(w / iw, h / ih)
        nw = int(iw * scale)
        nh = int(ih * scale)

        image = cv2.resize(image, (nw, nh))
        new_image = np.full((h, w, 3), 128, dtype=image.dtype)  # channels为3，仅jpg和三通道图

        new_image[(h - nh) // 2: (h - nh) // 2 + nh, (w - nw) // 2:(w - nw) // 2 + nw, :] = image
        # print(new_image.shape)
        return new_image

    def corp_margin(self, img):
        """
        图片去灰色边框操作
        :param img:
        :return:
        """
        img2 = img.sum(axis=2)
        (row, col) = img2.shape
        row_top = 0
        raw_down = 0
        col_top = 0
        col_down = 0
        for r in range(0, row):
            if img2.sum(axis=1)[r] != (128*3)*col:
                # 对channel维求和，灰条都是[128,128,128],如整列刚好相等则为灰条，不等则为正常区域，停止求边距
                row_top = r
                break
        for r in range(row-1, 0, -1):
            if img2.sum(axis=1)[r] != (128*3)*col:
                raw_down = r
                break
        for c in range(0, col):
            if img2.sum(axis=0)[c] != (128*3)*row:
                col_top = c
                break
        for c in range(col-1, 0, -1):
            if img2.sum(axis=0)[c] != (128*3)*row:
                col_down = c
                break
        new_img = img[row_top:raw_down+1, col_top:col_down+1, 0:3]
        return new_img