# -*- coding: utf-8 -*-
# @Time    : 2024/5/2 12:01
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : manage.py
# @Software: PyCharm

import os
import sys

from flask import make_response, jsonify

from app import create_app

# 默认为开发环境，按需求修改
config_name = 'development'

app = create_app(config_name)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'code': '404', 'msg': '接口不存在'}), 404)


@app.errorhandler(400)
def par_err(error):
    return make_response(jsonify({'code': '400', 'msg': '请求参数不合法'}), 400)


@app.route('/actuator/health', methods=['GET', 'HEAD'])
def health():
    return jsonify({'online': True})


if __name__ == '__main__':
    # 获取当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(current_file)
    # 将项目目录添加到 sys.path
    if base_dir not in sys.path:
        sys.path.append(base_dir)
    app.run(debug=True, host='0.0.0.0', port=5000)  # use_reloader=False, threaded=True,
