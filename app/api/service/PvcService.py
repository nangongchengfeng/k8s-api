# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:47
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : PvcService.py
# @Software: PyCharm
from app.api.models.PvcModels import Pvc


class Pvcs():
    def __init__(self):
        self.PC = Pvc()

    def disk(self, ns, name):
        try:
            res = self.PC.get(ns, name)
            data = res.spec.resources.requests['storage']
            return data
        except Exception as e:
            data = 0
            return data