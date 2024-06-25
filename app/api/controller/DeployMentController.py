# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 17:37
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : DeployMentController.py
# @Software: PyCharm
from flask import Blueprint, jsonify, request

from app.api.service.DeployMentService import Deployments

deploy = Blueprint('deployment', __name__)


@deploy.route('/<string:namespace>/Deployment', methods=['GET'])
def list_deployments(namespace):
    data = Deployments().list(namespace)
    return jsonify(data)


@deploy.route('/<string:namespace>/Deployment', methods=['POST'])
def create_deployments(namespace):
    list = ["name", "image", "type", "version", "cpu", "memory", "disk"]
    for i in list:
        if not i in request.json:
            data = {"code": 1, "msg": "缺少参数: {0}".format(i)}
            return jsonify(data)
    req = request.json
    name = req['name']
    image = req['image']
    version = req['version']
    cpu = req['cpu']
    memory = req['memory']
    disk = req['disk']
    stype = req['type']

    if stype == "app":
        data = Deployments().get(namespace, name)
    elif stype == "service":
        data = eval(image)().create(namespace, name, version, cpu, memory, disk)
    else:
        data = {"code": 1, "msg": "暂不支持的接口：{0}".format(stype)}

    return jsonify(data)


@deploy.route('/<string:namespace>/Deployment/<string:stype>/<string:name>', methods=['GET'])
def get_deployments(namespace, stype, name):
    if stype == "app":
        data = Deployments().get(namespace, name)
    else:
        data = eval(stype)().get(namespace, name)
    return jsonify(data)


@deploy.route('/<string:namespace>/Deployment/<string:stype>/<string:name>', methods=['DELETE'])
def del_deployments(namespace, stype, name):
    data = eval(stype)().delete(namespace, name)
    return jsonify(data)
