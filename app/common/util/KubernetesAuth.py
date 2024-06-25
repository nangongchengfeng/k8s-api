#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kubernetes import client, config
from datetime import timedelta, timezone
import os
import random
import string

from app.config import kubernetes_auth

"""
@author: Brian Chen
@file: Kubers
@time: 2020/9/4 16:44
"""


def Kubers():
    config.kube_config.load_kube_config(config_file=kubernetes_auth)
    return client


def UTC2CST(ucttime):
    dt = ucttime.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%S:%M")
    return dt


def GeneratePass():
    punctuation = "!@#$%^&*"
    a = string.ascii_letters + string.digits + punctuation
    key = random.sample(a, 12)
    keys = "".join(key)
    return keys
