import os
import os.path as osp

import pandas as pd
import numpy as np

from .files_op.operate import Files_op
#from .operate import Files_op

class Exc_op(Files_op):
    '''未完成'''
    def __new__(cls, *args, **kw):
        '''共享父类default属性'''
        ob = super().__new__(cls, *args, **kw)
        ob.default = cls.default
        ob.default.update({'Primarykey':''})
        return ob
    
    def __iter__(self):
        ...
    
    def createdf(self,rows,cols):
        df = pd.DataFrame(np.arange(rows*cols).reshape(rows,cols))
        return df
    
    def add_colname(self,df):
        return df
    
    def read(self,path,sheet_name='Sheet1',engine='openpyxl'):
        '''
        
        '''
        if osp.splitext(path)[-1]=='csv':
            df=pd.read_csv(path)
        else:
            df=pd.read_excel(path,sheet_name=sheet_name,engine=engine) #旧平台表路径
        return df
        
    def write(self,path,df,index=False,header=True):
        '''
        关键是csv不能手动打开，要用python，编码utf-8_sig保存，另存为xlsx格式就可以解决断行和中文乱码问题
        '''
        if osp.splitext(path)[-1]=='csv':
            
            #index参数设置为False表示不保存行索引,header设置为False表示不保存列索引
            df.to_csv(path,index=index,header=header,encoding='utf-8-sig')
        else:
            pass
        
    def add_column(self):
        ...
        
    def df2numpy(self):
        ...
