# -*- coding: utf-8 -*-
# @Time    : 2024-06-24 16:18
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : NamespaceController.py
# @Software: PyCharm
from flask import Blueprint, jsonify, request, abort

from app.api.service.NameSpaceService import Namespaces
from app.common.result.result import Result
from app.common.util.LogHandler import log

ns = Blueprint('namespace', __name__)


@ns.route('/namespace', methods=['GET'])
def list_ns():
    data = Namespaces().list()
    log.info("获取所有命名空间：{}".format(data))
    return jsonify(data)


@ns.route('namespace', methods=['POST'])
def create_ns():
    if not request.json or not 'name' in request.json or not 'cpu' in request.json or not 'memory' in request.json or not 'disk' in request.json:
        abort(400)
    req = request.json
    name = req['name']
    cpu = req['cpu']
    mem = req['memory']
    disk = req['disk']
    data = Namespaces().create(name, cpu, mem, disk)
    return jsonify(data)


@ns.route('namespace/<string:name>', methods=['GET'])
def get_ns(name):
    log.info("获取命名空间：{}".format(name))
    data = Namespaces().get(name)
    return jsonify(data)


@ns.route('namespace/<string:name>', methods=['PUT'])
def update_ns(name):
    if not request.json or not 'cpu' in request.json or not 'memory' in request.json or not 'disk' in request.json:
        abort(400)
    req = request.json
    cpu = req['cpu']
    mem = req['memory']
    disk = req['disk']
    data = Namespaces().update(name, cpu, mem, disk)
    return jsonify(data)


@ns.route('namespace/<string:name>', methods=['DELETE'])
def del_ns(name):
    data = Namespaces().delete(name)
    return jsonify(data)
