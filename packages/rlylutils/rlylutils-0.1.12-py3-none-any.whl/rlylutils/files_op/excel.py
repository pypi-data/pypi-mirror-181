import os
import os.path as osp

import pandas as pd
import numpy as np

from rlylutils.image.utils import *
from rlylutils.configs.cfg import Cfg
from rlylutils.decorators.decorators import Decorator
from rlylutils.files_op import Filesop

__all__ = ['Excop']


@Decorator.cdec(Cfg.default['param'])
class Excop(Filesop):

    def __new__(cls, *args, **kw):
        ob = super().__new__(cls, *args, **kw)
        ob.default = cls.default
        ob.default.update({'Primarykey': ''})
        return ob
    
    def __iter__(self):
        ...
    
    def create_df(self, rows, cols):
        self.df = pd.DataFrame(np.arange(rows*cols).reshape(rows, cols))
        return self.df
    
    def read(self, path, sheet_name='Sheet1', engine='openpyxl'):
        '''
        
        '''
        if osp.splitext(path)[-1] in ['.csv', '.tsv']:
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path, sheet_name=sheet_name, engine=engine)  # 旧平台表路径
        return df
        
    def write(self, path, index=False, header=True):
        '''
        关键是csv不能手动打开，要用python，编码utf-8_sig保存，另存为xlsx格式就可以解决断行和中文乱码问题
        '''
        if osp.splitext(path)[-1] == 'csv':
            
            # index参数设置为False表示不保存行索引,header设置为False表示不保存列索引
            self.df.to_csv(path, index=index, header=header, encoding='utf-8-sig')
        else:
            pass

    def list_colname(self):
        return self.df.columns.tolist()

    def vlookup(self, other_df, key_col_name, how='left'):
        return pd.merge(self.df, other_df, on=key_col_name, how=how)

    def filter(self, col_name, condition, val):
        """
        筛选
        :param col_name:
        :param condition:
        :param val:
        :return:
        """
        ...

    def sorted(self):
        ...

    def pivot(self):
        ...

    def summary(self):
        ...


    def add_column(self):
        ...
        
    def df2numpy(self):
        ...

    def numpy2df(self):
        ...

