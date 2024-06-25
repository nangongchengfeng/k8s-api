# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 16:31
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ResourceQuotaModels.py
# @Software: PyCharm
from app.common.util.KubernetesAuth import Kubers


class ResourceQuota():
    def __init__(self):
        self.Api = Kubers().CoreV1Api()

    def get(self, ns):
        data = self.Api.read_namespaced_resource_quota(name="default", namespace=ns)
        return data

    def create(self, ns, cpu, mem, disk):
        body = {
            "metadata": {
                "name": "default"
            },
            "spec": {
                "hard": {
                    "limits.cpu": cpu,
                    "limits.memory": mem,
                    "requests.cpu": cpu,
                    "requests.memory": mem,
                    "requests.storage": disk
                }
            }
        }
        data = self.Api.create_namespaced_resource_quota(namespace=ns, body=body)
        return data

    def update(self, ns, cpu, mem, disk):
        body = self.get(ns)
        body.spec.hard['limits.cpu'] = cpu
        body.spec.hard['limits.memory'] = mem
        body.spec.hard['requests.cpu'] = cpu
        body.spec.hard['requests.memory'] = mem
        body.spec.hard['requests.storage'] = disk
        data = self.Api.replace_namespaced_resource_quota(name="default", namespace=ns, body=body)
        return data
