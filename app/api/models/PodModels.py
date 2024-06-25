# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:51
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from app.common.util.KubernetesAuth import UTC2CST, Kubers


class Pod():
    def __init__(self):
        self.Api = Kubers().CoreV1Api()

    def list(self, ns):
        data = self.Api.list_namespaced_pod(namespace=ns)
        for i in data.items:
            i.metadata.creation_timestamp = UTC2CST(i.metadata.creation_timestamp)
        return data

    def get(self, ns, app, atype):
        lab = "app={app},type={type}".format(app=app, type=atype)
        data = self.Api.list_namespaced_pod(namespace=ns, label_selector=lab)
        for i in data.items:
            i.metadata.creation_timestamp = UTC2CST(i.metadata.creation_timestamp)
        return data