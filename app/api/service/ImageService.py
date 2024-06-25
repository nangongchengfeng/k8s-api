# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:58
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ImageService.py
# @Software: PyCharm

class Images():
    def __init__(self):
        self.IM = Image()

    def list(self, atype):
        try:
            res = self.IM.list(atype)
            d = []
            for i in res:
                d.append(i['name'].replace("service/", "").replace("cloud/", ""))

            data = {"code": 0, "msg": "查询成功", "data": d}
            return data
        except Exception as e:
            data = {"code": 1, "msg": "查询失败"}
            return data

    def get(self, type, name):
        try:
            res = self.IM.get(type, name)
            v = []
            for i in res:
                v.append(i["tags"][0]["name"])

            d = {"name": name, "version": sorted(v)}
            data = {"code": 0, "msg": "查询成功", "data": d}
            return data
        except Exception as e:
            data = {"code": 1, "msg": "查询失败"}
            return data