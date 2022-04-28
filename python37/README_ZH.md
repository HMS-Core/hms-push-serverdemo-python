## 华为推送服务服务端Python示例代码
[English](https://github.com/HMS-Core/hms-push-serverdemo-python/tree/master/python37) | 中文
## 目录
 * [简介](#简介)
 * [安装](#安装)
 * [环境要求](#环境要求)
 * [配置](#配置)
 * [示例代码](#示例代码)
 * [知识库](#知识库)
 * [授权许可](#授权许可)
 
## 简介

Python示例代码对华为推送服务（HUAWEI Push Kit）服务端接口进行封装，包含丰富的示例程序，方便您参考或直接使用。

示例代码主要包括以下组件：

| 包名     |    说明 |
| ----------   |    ------------|
| examples     |    示例代码包，每个包都可以独立运行 |
| push_admin   |    推送服务的服务端接口封装包 |
	
## 安装

安装本示例代码前，请解压zip文件包，并在解压后的文件目录中执行以下命令：
```
python setup.py install
```

## 环境要求
Python 2.7/3.7
JetBrains PyCharm（推荐使用）


## 配置 
initialize_app方法包括如下参数：

| 参数      |    说明 |
| -------------  |   ------------------------------------------------------------------------- |
| appid          |    应用ID，从应用消息中获取 |
| appsecret      |    应用访问密钥，从应用信息中获取 |
| token_server   |    华为OAuth 2.0获取token的地址。具体请参考[基于OAuth 2.0开放鉴权-客户端模式](https://developer.huawei.com/consumer/cn/doc/development/HMSCore-Guides/oauth2-0000001212610981)。|
| push_open_url  |    推送服务的访问地址。具体请参考[推送服务-下行消息](https://developer.huawei.com/consumer/cn/doc/development/HMSCore-Guides/android-server-dev-0000001050040110?ha_source=hms1)。|


## 示例代码

本示例代码以push_admin包中的Messaging结构体为入口。Messaging结构体中的方法完成了对推送服务服务端接口的调用。

Messaging包括如下方法:

| 方法             |     说明
| -----------------   |     --------------------------------------------------- |
| send_message        |     向设备发送消息 |
| subscribe_topic     |     订阅主题 |
| unsubscribe_topic   |     退订主题 |
| list_topics         |     查询设备订阅的主题列表 |
| initialize_app      |     初始化配置参数 |


1) 发送Android透传消息
代码位置: examples/send_data_message.py

2) 发送Android通知栏消息
代码位置: examples/send_notify_message.py

3) 基于主题发送消息
代码位置: examples/send_topic_message.py

4) 基于条件发送消息
代码位置: examples/send_condition_message.py

5) 向华为快应用发送消息
代码位置: examples/send_instance_app_message.py

6) 基于WebPush代理发送消息
代码位置: examples/send_webpush_message.py

7) 基于APNs代理发送消息
代码位置: examples/send_apns_message.py

8) 发送测试消息
代码位置: examples/send_test_message.py

## 知识库
| 知识库             |     地址
| -----------------   |     --------------------------------------------------- |
| requests            |     https://requests.readthedocs.io/en/master/ |
| six                 |     https://six.readthedocs.io/   |

## 授权许可
华为推送服务Python示例代码经过[Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0)授权许可。
