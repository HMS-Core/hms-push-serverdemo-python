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

from src.push_admin import initialize_app
from src.push_admin import messaging

notification = messaging.Notification(
    title='sample title',
    body='sample message body'
)

android_notification = messaging.AndroidNotification(
    icon='/raw/ic_launcher2',
    color='#AACCDD',
    sound='/raw/shake',
    default_sound=True,
    tag='tagBoom',
    click_action=messaging.AndroidClickAction(
        action_type=1,
        intent="intent://com.huawei.codelabpush/deeplink?#Intent;scheme=pushscheme;launchFlags=0x4000000;i.age=180;S.name=abc;end"),
    body_loc_key='M.String.body',
    body_loc_args=('boy', 'dog'),
    title_loc_key='M.String.title',
    title_loc_args=["Girl", "Cat"],
    channel_id='Your Channel ID',
    notify_summary='some summary',
    multi_lang_key={"title_key": {"en": "value1"}, "body_key": {"en": "value2"}},
    style=1,
    big_title='Big Boom Title',
    big_body='Big Boom Body',
    auto_clear=86400000,
    notify_id=486,
    group='Group1',
    importance=messaging.AndroidNotification.PRIORITY_HIGH,
    light_settings=messaging.AndroidLightSettings(color=messaging.AndroidLightSettingsColor(
                                                              alpha=0, red=0, green=1, blue=1)
                                                  , light_on_duration="3.5", light_off_duration="5S"),
    badge=messaging.AndroidBadgeNotification(
        add_num=1, clazz='Classic'),
    visibility=messaging.AndroidNotification.PUBLIC,
    foreground_show=True
)


android = messaging.AndroidConfig(
    collapse_key=-1,
    urgency=messaging.AndroidConfig.HIGH_PRIORITY,
    ttl="10000s",
    bi_tag='the_sample_bi_tag_for_receipt_service',
    notification=android_notification,
    category=None
)


def send_push_android_data_message():
    """
    a sample to show hwo to send web push message
    :return:
    """
    message = messaging.Message(
        notification=notification,
        android=android,
        # TODO
        topic='Your topic'
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
    """init sdk app"""
    # TODO
    app_id = "Your android application's app id"
    app_secret = "Your android application's app secret"
    initialize_app(app_id, app_secret)


def main():
    init_app()
    send_push_android_data_message()


if __name__ == '__main__':
    main()
