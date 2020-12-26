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

import json
from src import push_admin
from src.push_admin import messaging

web_push_headers = messaging.WebPushHeader(ttl="100")

web_push_notification = messaging.WebPushNotification(
    title="中文推送",
    body="中文推送内容中文推送内容中文推送内容中文推送内容中文推送内容中文推送内容中文推送内容中文推送内容中文推送内容",
    icon="https://developer-portalres-drcn.dbankcdn.com/system/modules/org.opencms.portal.template.core/\
         resources/images/icon_Promotion.png",
    actions=[messaging.WebPushNotificationAction(action="click", title="title", icon="https://developer-portalres-drcn.\
                dbankcdn.com/system/modules/org.opencms.portal.template.core/resources/images/icon_Promotion.png")],
    badge="badge",
    data="data",
    dir="auto",
    image="image url",
    lang="en",
    renotify=False,
    require_interaction=False,
    silent=True,
    tag="tag",
    timestamp=32323,
    vibrate=[1, 2, 3])

web_push_config = messaging.WebPushConfig(headers=web_push_headers, notification=web_push_notification)


def send_push_android_data_message():
    """
    a sample to show hwo to send web push message
    :return:
    """
    message = messaging.Message(
        web_push=web_push_config,
        # TODO
        token=['your token']
    )

    try:
        # Case 1: Local CA sample code
        # response = messaging.send_message(message, verify_peer="../Push-CA-Root.pem")
        # Case 2: No verification of HTTPS's certificate
        response = messaging.send_message(message)
        # Case 3: use certifi Library
        # import certifi
        # response = messaging.send_message(message, verify_peer=certifi.where())
        print("response is ", json.dumps(vars(response)))
        assert (response.code == '80000000')
    except Exception as e:
        print(repr(e))


def init_app():
    """init sdk app
    The appID & app Secret use the Android's application ID and Secret under the same project, next version you can use
    the web application's own appId & secret!
    """
    # TODO
    app_id_at = "Your android application's app id"
    app_secret_at = "Your android application's app secret"
    app_id_push = "Your Web application' app id "
    push_admin.initialize_app(app_id_at, app_secret_at, app_id_push)


def main():
    init_app()
    send_push_android_data_message()


if __name__ == '__main__':
    main()
