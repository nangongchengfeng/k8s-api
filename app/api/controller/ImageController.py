# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:56
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ImageController.py
# @Software: PyCharm
from flask import jsonify, Blueprint

from app.api.service.ImageService import Images

image = Blueprint('image', __name__)

"""
根据类仓库名称获取镜像列表
可选参数：type：   app  或 service   只允许访问这两个类型的镜像仓库
"""


@image.route('/<string:type>', methods=['GET'])
def list_image(type):
    data = Images().list(type)
    return jsonify(data)


@image.route('/<string:type>/<string:name>', methods=['GET'])
def get_image(type, name):
    """
    根据类仓库名称和镜像名称获取镜像信息
    :param type:
    :param name:
    :return:

    """
    data = Images().get(type, name)
    return jsonify(data)
