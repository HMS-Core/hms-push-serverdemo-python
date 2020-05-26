# -*- coding: utf-8 -*-
#
# Copyright 2020. Huawei Technologies Co., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests


def post(url, req_body, headers=None):
    """ post http request to slb service
        :param url: url path
        :param req_body: http request body
        :param headers: http headers
        :return:
            success return response
            fali return None
    """
    try:
        response = requests.post(url, data=req_body, headers=headers, timeout=10, verify=False)
        return response

    except Exception as e:
        raise ValueError('caught exception when post {0}. {1}'.format(url, e))


def _format_http_text(method, url, headers, body):
    """
    print http head and body for request or response

    For examples: _format_http_text('', title, response.headers, response.text)
    """
    result = method + ' ' + url + '\n'

    if headers is not None:
        for key, value in headers.items():
            result = result + key + ': ' + value + '\n'

    result = result + body
    return result


