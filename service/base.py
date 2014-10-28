#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'
__doc__ = 'ring info remote api interface base.'

import os
import time
import json
import random
import os.path
import requests

import urllib
# import base64
# import urllib2,urllib3

from .conf import DEBUG, JSON_HEADER, DIR_DOWNLOAD_FILES


def check_file_dir(dir_path):
    u"""检查目录是否存在, 若不存在创建.
    """

    os.path.isdir(dir_path)

    def create_path(my_path):
        if not os.path.exists(my_path):
            os.mkdir(my_path)

        if os.path.exists(my_path):
            return my_path
        else:
            return create_path(my_path)

    if DIR_DOWNLOAD_FILES:
        return create_path(DIR_DOWNLOAD_FILES)
    else:
        return create_path(dir_path)


def build_file_rename(file_name):
    u"""本地文件上传异地重命名
    """

    str_file_suf = file_name.split('.')[-1]
    str_time_rnd = '_'.join((str(int(time.time())), str(random.randint(10000, 99999))))

    return '.'.join((str_time_rnd, str_file_suf))


def build_query_url(url, dict_data):
    u"""构建get形式的请求地址

        :dict_data:dict形式的query数据
    """

    # urllib.urlencode() 不幸的是, 这个函数只能接收key-value pair格式的数据, 即只针对dict的.
    params = urllib.urlencode(dict_data)
    return "%s?%s" % (url, params)


def build_query_string(ql=None):
    u"""构建sql query 的查询urlencode
    """

    result = ''

    if ql:
        result = "?" + "ql=%s" % urllib.quote(ql)
        # result = "?" + "ql=%s" % urllib.unquote(ql)
        # result = "?" + "ql=%s" % base64.urlsafe_b64encode(ql)  # urlsafe_b64encode 接不上REST API

    return result


def check_ring_id(ring_id):
    u"""检测环信ID

        环信ID需要使用英文字母和（或）数字的组合
        环信ID不能使用中文
        环信ID不能使用email地址
        环信ID不能使用UUID
        环信ID中间不能有空格或者井号（#）等特殊字符
    """

    print str(ring_id)

    pass


def put(url, payload, auth=None):
    u"""构建put请求
    """
    r = requests.put(url, data=json.dumps(payload), headers=JSON_HEADER, auth=auth)
    return http_result(r)


def post(url, payload, auth=None):
    u"""构建Post请求
    """
    r = requests.post(url, data=json.dumps(payload), headers=JSON_HEADER, auth=auth)
    return http_result(r)


def get(url, auth=None):
    u"""构建Get请求
    """
    r = requests.get(url, headers=JSON_HEADER, auth=auth)
    return http_result(r)


def delete(url, auth=None):
    u"""构建Delete请求
    """
    r = requests.delete(url, headers=JSON_HEADER, auth=auth)
    return http_result(r)


def http_result(r):
    if DEBUG:
        error_log = {
            "method": r.request.method,
            "url": r.request.url,
            "request_header": dict(r.request.headers),
            "response_header": dict(r.headers),
            "response": r.text
        }
        if r.request.body:
            error_log["payload"] = r.request.body
            # print json.dumps(error_log)

    if r.status_code == requests.codes.ok:
        return True, r.json()
    else:
        return False, r.text
