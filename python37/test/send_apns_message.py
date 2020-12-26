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

from src import push_admin
import json
from src.push_admin  import messaging


headers = {messaging.APNsHeader.HEAD_APNs_ID: "6532dc0e-f581-7bfb-e1ab-60ec3cecea73"}

apns_alert = messaging.APNsAlert(title="HMS Push Title",
                                 body="HMS Push Body",
                                 launch_image="Default.png",
                                 custom_data={"k1": "v1", "k2": "v2"})

apns_payload_aps = messaging.APNsAps(alert=apns_alert,
                                     badge=1,
                                     sound="wtewt.mp4",
                                     content_available=True,
                                     category="category",
                                     thread_id="id")

payload = messaging.APNsPayload(aps=apns_payload_aps,
                                acme_account="jane.appleseed@apple.com",
                                acme_message="message123456")

apns_hms_options = messaging.APNsHMSOptions(target_user_type=1)

apns_push_config = messaging.APNsConfig(headers=headers,
                                        payload=payload,
                                        apns_hms_options=apns_hms_options)


def send_apns_push_message():
    """
    a sample to show hwo to send web push message
    :return:
    """
    message = messaging.Message(
        apns=apns_push_config,
        # TODO：
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
    """init sdk app. The appID & app Secret use the Android's application ID and Secret under the same project, next version you can use
    the IOS application's own appId & secret! """
    # TODO：
    app_id_at = "Your android application's app id"
    app_secret_at = "Your android application's app secret"
    app_id_push = "Your IOS application' app id "
    push_admin.initialize_app(app_id_at, app_secret_at, app_id_push)


def main():
    init_app()
    send_apns_push_message()


if __name__ == '__main__':
    main()
