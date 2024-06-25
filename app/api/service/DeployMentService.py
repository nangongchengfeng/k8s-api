# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:39
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : DeployMentService.py
# @Software: PyCharm
from app.api.models.DeployMentModels import Deployment
from app.api.models.PodModels import Pod
from app.api.service.PvcService import Pvcs


class Deployments():
    def __init__(self):
        self.DP = Deployment()

    def ns_filter(self, ns):
        filter = ["default", "dev", "fws", "fat", "uat", "ingress-nginx", "kube-node-lease", "kube-public",
                  "kube-system"]

        if ns in filter:
            return True
        else:
            return False

    def unit_con(self, data):
        if 'Mi' in data:
            data = int(data.replace('Mi', '')) / 1000
        elif 'Gi' in data:
            data = int(data.replace('Gi', ''))
        elif 'm' in data:
            data = int(data.replace('m', '')) / 1000
        else:
            data = int(data)
        return data

    def get_resources(self, data):
        cpu = 0
        mem = 0
        disk = 0
        for i in data.spec.template.spec.containers:
            if 'cpu' in i.resources.limits:
                cpu += self.unit_con(i.resources.limits['cpu'])
            else:
                cpu += 0

            if 'memory' in i.resources.limits:
                mem += self.unit_con(i.resources.limits['memory'])
            else:
                mem += 0

        if data.spec.template.spec.volumes is None:
            disk += 0
        else:
            for i in data.spec.template.spec.volumes:
                if i.persistent_volume_claim is None:
                    disk += 0
                else:
                    disk_res = Pvcs().disk(ns=data.metadata.namespace, name=data.metadata.name)
                    disk += self.unit_con(disk_res)
        data = {"cpu": str(cpu), "mem": str(mem), "disk": str(disk)}
        return data

    def list(self, ns):
        try:
            res = self.DP.list(ns)
            d_l = []
            for i in res.items:
                resource_data = self.get_resources(i)
                if "type" in i.metadata.labels:
                    type = i.metadata.labels['type']
                else:
                    type = ""

                if "version" in i.metadata.labels:
                    version = i.metadata.labels['version']
                else:
                    version = ""

                d = {
                    "name": i.metadata.name,
                    "type": type,
                    "version": version,
                    "createtime": i.metadata.creation_timestamp,
                    "resources": "{0}c|{1}G|{2}G".format(resource_data['cpu'], resource_data['mem'],
                                                         resource_data['disk'])
                }
                d_l.append(d)
            data = {"code": 0, "msg": "查询成功", "data": d_l}
            return data
        except Exception as e:
            print(e)
            data = {"code": 1, "msg": "查询失败"}
            return data

    def get(self, ns, name):
        try:
            res = self.DP.get(ns, name)
            if res.metadata.labels['type'] == "app":
                d_l = []
                pods = Pod().get(ns, name, "app")
                pod = []

                for i in pods.items:
                    p = {
                        "name": i.metadata.name,
                        "createtime": i.metadata.creation_timestamp,
                        "ip": i.status.pod_ip,
                        "status": i.status.phase
                    }
                    pod.append(p)

                for i in res.spec.template.spec.containers:
                    ports = []
                    if i.ports is not None:
                        for p in i.ports:
                            ports.append(p.container_port)
                    s_d = {
                        "name": i.name,
                        "ports": ports,
                        "resources": i.resources.limits
                    }
                    d_l.append(s_d)

                d = {
                    "name": res.metadata.name,
                    "createtime": res.metadata.creation_timestamp,
                    "number": "{0}/{1}".format(res.status.ready_replicas, res.status.replicas),
                    "host": "{0}.{1}.svc.cloudcs.fjf".format(res.metadata.name, res.metadata.namespace),
                    "service": d_l,
                    "pods": pod
                }

                data = {"code": 0, "msg": "查询成功", "data": d}
                return data
            else:
                data = {"code": 1, "msg": "查询失败,仅支持app类型"}
                return data
        except Exception as e:
            data = {"code": 1, "msg": "查询失败"}
            return data
