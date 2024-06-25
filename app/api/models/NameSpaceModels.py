# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 16:23
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : NameSpaceModels.py
# @Software: PyCharm
from app.common.util.KubernetesAuth import Kubers, UTC2CST


class Namespace():
    def __init__(self):
        self.Api = Kubers().CoreV1Api()

    def list(self):
        data = self.Api.list_namespace()
        return data

    def get(self, ns):
        data = self.Api.read_namespace(name=ns)
        data.metadata.creation_timestamp = UTC2CST(data.metadata.creation_timestamp)
        return data

    def create(self, ns):
        body = {
            "metadata": {
                "name": ns
            }
        }
        data = self.Api.create_namespace(body=body)
        return data

    def delete(self, ns):
        data = self.Api.delete_namespace(name=ns)
        return data
