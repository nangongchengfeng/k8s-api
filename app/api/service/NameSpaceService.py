# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 16:22
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : NameSpaceService.py
# @Software: PyCharm
from app.api.models.NameSpaceModels import Namespace
from app.api.models.ResourceQuotaModels import ResourceQuota
from app.common.util.LogHandler import log


class Namespaces():
    def __init__(self):
        self.NS = Namespace()
        self.RQ = ResourceQuota()

    def ns_filter(self, ns):
        filter = ["default", "dev", "fws", "fat", "uat", "ingress-nginx", "kube-node-lease", "kube-public",
                  "kube-system"]

        if ns in filter:
            return True
        else:
            return False

    def unit_con(self, data):
        if 'Mi' in data:
            data = str(int(data.replace('Mi', '')) / 1000)
        elif 'Gi' in data:
            data = data.replace('Gi', '')
        elif 'm' in data:
            data = str(int(data.replace('m', '')) / 1000)
        return data

    def list(self):
        try:
            res = self.NS.list()
            nl = []
            for i in res.items:
                if not self.ns_filter(i.metadata.name):
                    nl.append(i.metadata.name)
            data = {"code": 0, "msg": "", "data": nl}
            return data
        except Exception as e:
            data = {"code": 1, "msg": "请求失败"}
            return data

    def get(self, ns):
        log.info("获取命名空间的相关信息：{}".format(ns))
        try:
            if self.ns_filter(ns):
                data = {"code": 1, "msg": "禁止查询"}
                return data

            ns_res = self.NS.get(ns)
            print("===================", ns_res)

            ctime = ns_res.metadata.creation_timestamp
            status = ns_res.status.phase
            labels = ns_res.metadata.labels
            print("===================", ctime, status)
            rq_res = self.RQ.get(ns)
            cpu_limit = rq_res.status.hard['limits.cpu']
            mem_limit = self.unit_con(rq_res.status.hard['limits.memory'])
            disk_limit = self.unit_con(rq_res.status.hard['requests.storage'])
            cpu_used = self.unit_con(rq_res.status.used['limits.cpu'])
            mem_used = self.unit_con(rq_res.status.used['limits.memory'])
            disk_used = self.unit_con(rq_res.status.used['requests.storage'])

            data = {
                "code": 0,
                "msg": "查询成功",
                "data": {
                    "createtime": ctime,
                    "status": status,
                    "total": {
                        "cpu": cpu_limit,
                        "memory": mem_limit,
                        "disk": disk_limit
                    },
                    "used": {
                        "cpu": cpu_used,
                        "memory": mem_used,
                        "disk": disk_used
                    }
                }
            }
            return data
        except Exception as e:

            data = {"code": 1, "msg": "查询失败,请检查命名空间是否设置资源配额"}
            log.error("获取命名空间的相关信息失败：{}".format(data))
            return data

    def create(self, ns, cpu, mem, disk):
        try:
            if self.ns_filter(ns):
                data = {"code": 1, "msg": "禁止创建"}
                return data
            mem = mem + "Gi"
            disk = disk + "Gi"
            self.NS.create(ns)
            self.RQ.create(ns, cpu, mem, disk)
            data = {"code": 0, "msg": "创建成功"}
            return data
        except Exception as e:
            data = {"code": 1, "msg": "创建失败"}
            return data

    def delete(self, ns):
        try:
            if self.ns_filter(ns):
                data = {"code": 1, "msg": "禁止删除"}
                return data

            self.NS.delete(ns)
            data = {"code": 0, "msg": "删除成功"}
            return data
        except Exception as e:
            data = {"code": 1, "msg": "删除失败"}
            return data

    def update(self, ns, cpu, mem, disk):
        try:
            if self.ns_filter(ns):
                data = {"code": 1, "msg": "禁止更新"}
                return data
            self.RQ.update(ns, cpu, mem, disk)
            data = {"code": 0, "msg": "更新成功"}
            return data
        except Exception as e:
            data = {"code": 1, "msg": "更新失败"}
            return data
