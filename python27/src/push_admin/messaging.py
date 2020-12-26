# -*-coding:utf-8-*-
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

from src.push_admin import _messages, _app
from src import push_admin

"""HUAWEI Cloud Messaging module."""

""" General Data structure """
Message = _messages.Message
Notification = _messages.Notification

""" Web Push related data structure """
WebPushConfig = _messages.WebPushConfig
WebPushHeader = _messages.WebPushHeader
WebPushNotification = _messages.WebPushNotification
WebPushNotificationAction = _messages.WebPushNotificationAction
WebPushHMSOptions = _messages.WebPushHMSOptions

""" Android Push related data structure """
AndroidConfig = _messages.AndroidConfig
AndroidNotification = _messages.AndroidNotification
AndroidClickAction = _messages.AndroidClickAction
AndroidBadgeNotification = _messages.AndroidBadgeNotification
AndroidLightSettings = _messages.AndroidLightSettings
AndroidLightSettingsColor = _messages.AndroidLightSettingsColor

""" APNS Push related data structure"""
APNsConfig = _messages.APNsConfig
APNsHeader = _messages.APNsHeader
APNsPayload = _messages.APNsPayload
APNsAps = _messages.APNsAps
APNsAlert = _messages.APNsAlert
APNsHMSOptions = _messages.APNsHMSOptions

"""Common exception definition"""
ApiCallError = _app.ApiCallError


def send_message(message, validate_only=False, app_id=None, verify_peer=False):
    """
        Sends the given message Huawei Cloud Messaging (HCM)
        :param message: An instance of ``messaging.Message``.
        :param validate_only: A boolean indicating whether to run the operation in dry run mode (optional).
        :param app_id: app id parameters obtained by developer alliance applying for Push service (optional).
        :param verify_peer: (optional) Either a boolean, in which case it controls whether we verify
            the server's TLS certificate, or a string, in which case it must be a path
            to a CA bundle to use. Defaults to ``True``.
        :return: SendResponse
        Raises:
            ApiCallError: If an error occurs while sending the message to the HCM service.
    """
    try:
        response = push_admin.get_app(app_id).send(message, validate_only, verify_peer=verify_peer)
        return SendResponse(response)
    except Exception as e:
        raise ApiCallError(repr(e))


def subscribe_topic(topic, token_list, app_id=None):
    """
    :param topic: The specific topic
    :param token_list: The token list to be added
    :param app_id: application ID
    """
    try:
        response = push_admin.get_app(app_id).subscribe_topic(topic, token_list)
        return TopicSubscribeResponse(response)
    except Exception as e:
        raise ApiCallError(repr(e))


def unsubscribe_topic(topic, token_list, app_id=None):
    """
    :param topic: The specific topic
    :param token_list: The token list to be deleted
    :param app_id: application ID
    """
    try:
        response = push_admin.get_app(app_id).unsubscribe_topic(topic, token_list)
        return TopicSubscribeResponse(response)
    except Exception as e:
        raise ApiCallError(repr(e))


def list_topics(token, app_id=None):
    """
    :param token: The token to be queried
    :param app_id: application ID
    """
    try:
        response = push_admin.get_app(app_id).query_subscribe_list(token)
        return TopicQueryResponse(response)
    except Exception as e:
        raise ApiCallError(repr(e))


class SendResponse(object):
    """
        The response received from an send request to the HCM API.
        response: received http response body text from HCM.
    """
    def __init__(self, response=None):
        try:
            self._msg = response['msg']
            self._code = response['code']
            self._requestId = response['requestId']
        except Exception as e:
            raise ValueError(format(repr(e)))

    @property
    def code(self):
        """errcode"""
        return self._code

    @property
    def reason(self):
        """the description of errcode"""
        return self._msg

    @property
    def requestId(self):
        """A message ID string that uniquely identifies the message."""
        return self._requestId


class BaseTopicResponse(object):
    """
    {
       "msg": "Success",
       "code": "80000000",
       "requestId": "157466304904000004000701"
     }
    """
    def __init__(self, json_rsp=None):
        if json_rsp is None:
            self._msg = ""
            self._code = ""
            self._requestId = ""
        else:
            self._msg = json_rsp['msg']
            self._code = json_rsp['code']
            self._requestId = json_rsp['requestId']

    @property
    def msg(self):
        return self._msg

    @property
    def code(self):
        return self._code

    @property
    def requestId(self):
        return self._requestId


class TopicSubscribeResponse(BaseTopicResponse):
    """
     {
       "msg": "Success",
       "code": "80000000",
       "requestId": "157466304904000004000701",
       "successCount": 2,
       "failureCount": 0,
       "errors": []
     }
    """
    def __init__(self, json_rsp=None):
        super(TopicSubscribeResponse, self).__init__(json_rsp=json_rsp)
        if json_rsp is None:
            self._successCount = 0
            self._failureCount = 0
            self._errors = []
        else:
            self._successCount = json_rsp['successCount']
            self._failureCount = json_rsp['failureCount']
            self._errors = json_rsp['errors']

    @property
    def successCount(self):
        return self._successCount

    @property
    def failureCount(self):
        return self._failureCount

    @property
    def errors(self):
        return self._errors


class TopicQueryResponse(BaseTopicResponse):
    """
         {
           "msg": "success",
           "code": "80000000",
           "requestId": "157466350121600008000701",
           "topics": [
                       { "name": "sports",
                         "addDate": "2019-11-25"
                         } ]
         }
    """
    def __init__(self, json_rsp=None):
        super(TopicQueryResponse, self).__init__(json_rsp)
        self._topics = json_rsp['topics']

    @property
    def topics(self):
        return self._topics
