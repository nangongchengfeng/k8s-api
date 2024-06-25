# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:40
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
from app.common.util.KubernetesAuth import UTC2CST, Kubers


class Deployment():
    def __init__(self):
        self.Api = Kubers().AppsV1Api()

    def list(self, ns):
        data = self.Api.list_namespaced_deployment(namespace=ns)
        for i in data.items:
            i.metadata.creation_timestamp = UTC2CST(i.metadata.creation_timestamp)
        return data

    def get(self, ns, name):
        data = self.Api.read_namespaced_deployment(namespace=ns, name=name)
        data.metadata.creation_timestamp = UTC2CST(data.metadata.creation_timestamp)
        return data

    def create(self, ns, name):
        body = {
            "metadata": {
                "name": name
            },
            "spec": {}
        }
        data = self.Api.create_namespaced_deployment(namespace=ns, body=body)
        return data
