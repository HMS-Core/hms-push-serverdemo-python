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

import urllib
import json
import time
from src.push_admin import _http
from src.push_admin import _message_serializer


class App(object):
    """application for HW Cloud Message(HCM)"""

    JSON_ENCODER = _message_serializer.MessageSerializer()

    @classmethod
    def _send_to_server(cls, headers, body, url, verify_peer=False):
        try:
            msg_body = json.dumps(body)
            response = _http.post(url, msg_body, headers, verify_peer)

            if response.status_code is not 200:
                raise ApiCallError('http status code is {0} in send.'.format(response.status_code))

            # json text to dict
            resp_dict = json.loads(response.text)
            return resp_dict

        except Exception as e:
            raise ApiCallError('caught exception when send. {0}'.format(e))

    def __init__(self, appid_at, app_secret, appid_push, token_server='https://oauth-login.cloud.huawei.com/oauth2/v3/token',
                 push_open_url='https://push-api.cloud.huawei.com'):
        """class init"""
        self.appid_at = appid_at
        self.app_secret_at = app_secret
        if appid_push is None:
            self.appid_push = appid_at
        else:
            self.appid_push = appid_push
        self.token_expired_time = 0
        self.access_token = None
        self.token_server = token_server
        self.push_open_url = push_open_url
        self.hw_push_server = self.push_open_url + "/v1/{0}/messages:send"
        self.hw_push_topic_sub_server = self.push_open_url + "/v1/{0}/topic:subscribe"
        self.hw_push_topic_unsub_server = self.push_open_url + "/v1/{0}/topic:unsubscribe"
        self.hw_push_topic_query_server = self.push_open_url + "/v1/{0}/topic:list"

    def _refresh_token(self, verify_peer=False):
        """refresh access token
        :param verify_peer: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        """
        headers = dict()
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'

        params = dict()
        params['grant_type'] = 'client_credentials'
        params['client_secret'] = self.app_secret_at
        params['client_id'] = self.appid_at

        msg_body = urllib.urlencode(params)

        try:
            response = _http.post(self.token_server, msg_body, headers, verify_peer=verify_peer)

            if response.status_code is not 200:
                return False, 'http status code is {0} in get access token'.format(response.status_code)

            """ json string to directory """
            response_body = json.loads(response.text)

            self.access_token = response_body.get('access_token')
            self.token_expired_time = long(round(time.time() * 1000)) + (long(response_body.get('expires_in')) - 5 * 60) * 1000

            return True, None
        except Exception as e:
            raise ApiCallError(format(repr(e)))

    def _is_token_expired(self):
        """is access token expired"""
        if self.access_token is None:
            """ need refresh token """
            return True
        return long(round(time.time() * 1000)) >= self.token_expired_time

    def _update_token(self, verify_peer=False):
        if self._is_token_expired() is True:
            result, reason = self._refresh_token(verify_peer)
            if result is False:
                raise ApiCallError(reason)

    def _create_header(self):
        headers = dict()
        headers['Content-Type'] = 'application/json;charset=utf-8'
        headers['Authorization'] = 'Bearer {0}'.format(self.access_token)
        return headers

    def send(self, message, validate_only, **kwargs):
        """
            Sends the given message Huawei Cloud Messaging (HCM)
            :param message:
            :param validate_only:
            :param kwargs:
                   verify_peer: HTTPS server identity verification, use library 'certifi'
            :return:
                response dict: response body dict
            :raise:
                ApiCallError: failure reason
        """
        verify_peer = kwargs['verify_peer']
        self._update_token(verify_peer)
        headers = self._create_header()
        url = self.hw_push_server.format(self.appid_push)
        msg_body_dict = dict()
        msg_body_dict['validate_only'] = validate_only
        msg_body_dict['message'] = App.JSON_ENCODER.default(message)

        return App._send_to_server(headers, msg_body_dict, url, verify_peer)

    def subscribe_topic(self, topic, token_list):
        """
        :param topic: The specific topic
        :param token_list: The token list to be added
        :return:
        """
        self._update_token()
        headers = self._create_header()
        url = self.hw_push_topic_sub_server.format(self.appid_push)
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
        url = self.hw_push_topic_unsub_server.format(self.appid_push)
        msg_body_dict = {'topic': topic, 'tokenArray': token_list}
        return App._send_to_server(headers, msg_body_dict, url)

    def query_subscribe_list(self, token):
        """
        :param token:  The specific token
        :return:
        """
        self._update_token()
        headers = self._create_header()
        url = self.hw_push_topic_query_server.format(self.appid_push)
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
