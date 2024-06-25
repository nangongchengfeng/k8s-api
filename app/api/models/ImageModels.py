# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:58
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ImageModels.py
# @Software: PyCharm


"""
images class的初始化函数，初始化镜像仓库的用户名和密码，基本信息
"""
import base64

import requests


class Image():
    def __init__(self):
        self.host = "bdata-hub.xxxxxx.cn"
        self.username = "admin"
        self.password = "xxxxxx"

    """
    使用requests库发送请求，获取镜像仓库的token，用于后续的请求，获取信息
    """

    def req(self, url):
        user_info_str = self.username + ":" + self.password
        user_info = base64.b64encode(user_info_str.encode())
        headers = {"Authorization": "Basic " + user_info.decode()}
        url = "https://" + self.host + url
        data = requests.get(url, headers=headers).json()
        return data

    """
    实现仓库的过滤，只允许访问app和service类型的镜像仓库
    """

    def tyep_url(self, type):
        if type == "app":
            url = "/api/v2.0/projects/cloud/repositories"
        else:
            url = "/api/v2.0/projects/service/repositories"
        return url

    def list(self, type):
        url = self.tyep_url(type)
        data = self.req(url)
        return data

    """
    获取镜像仓库中指定镜像的信息
    """

    def get(self, type, name):
        url = self.tyep_url(type)
        url = url + "/" + name + "/artifacts"
        data = self.req(url)
        return data
