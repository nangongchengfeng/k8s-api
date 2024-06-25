# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:48
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : PvcModels.py
# @Software: PyCharm


class Pvc():
    def __init__(self):
        self.Api = Kubers().CoreV1Api()

    def get(self, ns, name):
        data = self.Api.read_namespaced_persistent_volume_claim(namespace=ns, name=name)
        data.metadata.creation_timestamp = UTC2CST(data.metadata.creation_timestamp)
        return data

    def create(self, ns, name, size):
        body = {
            "metadata": {
                "name": name,
                "annotations": {
                    "volume.beta.kubernetes.io/storage-class": "managed-nfs-storage"
                },
            },
            "spec": {
                "accessModes": [
                    "ReadWriteMany"
                ],
                "resources": {
                    "requests": {
                        "storage": size
                    }
                }
            }
        }
        data = self.Api.create_namespaced_persistent_volume_claim(namespace=ns, body=body)
        return data

    def delete(self, ns, name):
        data = self.Api.delete_namespaced_persistent_volume_claim(namespace=ns, name=name)
        return data
