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

import urllib.parse
import json
import time
from src.push_admin import _http
from src.push_admin import _message_serializer


class App(object):
    """application for HW Cloud Message(HCM)"""

    JSON_ENCODER = _message_serializer.MessageSerializer()

    @classmethod
    def _send_to_server(cls, headers, body, url):
        try:
            msg_body = json.dumps(body)
            response = _http.post(url, msg_body, headers)

            if response.status_code is not 200:
                raise ApiCallError('http status code is {0} in send.'.format(response.status_code))

            # json text to dict
            resp_dict = json.loads(response.text)
            return resp_dict

        except Exception as e:
            raise ApiCallError('caught exception when send. {0}'.format(e))

    def __init__(self, app_id, app_secret, token_server='https://oauth-login.cloud.huawei.com/oauth2/v2/token',
                 push_open_url='https://push-api.cloud.huawei.com'):
        """class init"""
        self.app_id = app_id
        self.app_secret = app_secret
        self.token_expired_time = 0
        self.access_token = None
        self.token_server = token_server
        self.push_open_url = push_open_url
        self.hw_push_server = self.push_open_url + "/v1/{0}/messages:send"
        self.hw_push_topic_sub_server = self.push_open_url + "/v1/{0}/topic:subscribe"
        self.hw_push_topic_unsub_server = self.push_open_url + "/v1/{0}/topic:unsubscribe"
        self.hw_push_topic_query_server = self.push_open_url + "/v1/{0}/topic:list"

    def _refresh_token(self):
        """refresh access token"""
        headers = dict()
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'

        params = dict()
        params['grant_type'] = 'client_credentials'
        params['client_secret'] = self.app_secret
        params['client_id'] = self.app_id

        msg_body = urllib.parse.urlencode(params)

        try:
            response = _http.post(self.token_server, msg_body, headers)

            if response.status_code is not 200:
                return False, 'http status code is {0} in get access token'.format(response.status_code)

            """ json string to directory """
            response_body = json.loads(response.text)

            self.access_token = response_body.get('access_token')
            self.token_expired_time = int(round(time.time() * 1000)) + (int(response_body.get('expires_in')) - 5 * 60) * 1000

            return True, None
        except Exception as e:
            raise ApiCallError(format(repr(e)))

    def _is_token_expired(self):
        """is access token expired"""
        if self.access_token is None:
            """ need refresh token """
            return True
        return int(round(time.time() * 1000)) >= self.token_expired_time

    def _update_token(self):
        if self._is_token_expired() is True:
            result, reason = self._refresh_token()
            if result is False:
                raise ApiCallError(reason)

    def _create_header(self):
        headers = dict()
        headers['Content-Type'] = 'application/json;charset=utf-8'
        headers['Authorization'] = 'Bearer {0}'.format(self.access_token)
        return headers

    def send(self, message, validate_only):
        """
            Sends the given message Huawei Cloud Messaging (HCM)
            :param message:
            :param validate_only:
            :return:
                response dict: response body dict
            :raise:
                ApiCallError: failure reason
        """
        self._update_token()
        headers = self._create_header()
        url = self.hw_push_server.format(self.app_id)
        msg_body_dict = dict()
        msg_body_dict['validate_only'] = validate_only
        msg_body_dict['message'] = App.JSON_ENCODER.default(message)

        return App._send_to_server(headers, msg_body_dict, url)

    def subscribe_topic(self, topic, token_list):
        """
        :param topic: The specific topic
        :param token_list: The token list to be added
        :return:
        """
        self._update_token()
        headers = self._create_header()
        url = self.hw_push_topic_sub_server.format(self.app_id)
        msg_body_dict = {'topic': topic, 'tokenArray': token_list}
        return App._send_to_server(headers, msg_body_dict, url)

    def unsubscribe_topic(self, topic, token_list):
        """

        :param topic: The specific topic
        :param token_list: The token list to be deleted
        :return:
        """
        self._update_token()
        headers = self._create_header()
        url = self.hw_push_topic_unsub_server.format(self.app_id)
        msg_body_dict = {'topic': topic, 'tokenArray': token_list}
        return App._send_to_server(headers, msg_body_dict, url)

    def query_subscribe_list(self, token):
        """
        :param token:  The specific token
        :return:
        """
        self._update_token()
        headers = self._create_header()
        url = self.hw_push_topic_query_server.format(self.app_id)
        msg_body_dict = {'token': token}
        return App._send_to_server(headers, msg_body_dict, url)


class ApiCallError(Exception):
    """Represents an Exception encountered while invoking the HCM API.

    Attributes:
        message: A error message string.
        detail: Original low-level exception.
    """
    def __init__(self, message, detail=None):
        Exception.__init__(self, message)
        self.detail = detail
