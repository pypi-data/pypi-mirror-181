# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@version    : v1.0
@author     : fangzheng
@contact    : fangzheng@yourtools-pet.cn
@software   : PyCharm
@filename   : mysql.py
@create time: 2022/9/17 6:58 PM
@modify time: 2022/9/17 6:58 PM
@describe   :
-------------------------------------------------
"""


class DBConfig:
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
        if not hasattr(self, 'charset'):
            self.charset = 'utf8'
