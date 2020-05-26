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
#
# refer. https://wiki.python.org/moin/Distutils/Tutorial?highlight=%28setup.py%29
#
from setuptools import setup

__version__ = '1.0.0'
__title__ = 'hcm_admin'
__author__ = 'Huawei'
__license__ = 'Apache License 2.0'
__url__ = 'https://developer.huawei.com/consumer/cn/'

install_requires = ['requests>=2.20.1']

long_description = ('The Huawei Admin Python SDK enables server-side (backend) Python developers '
                    'to integrate Huawei into their services and applications.')

setup(
    name='huawei_push_admin',
    version='1.0.0',
    description='Huawei Admin Python SDK',
    long_description=long_description,
    url='https://developer.huawei.com/consumer/cn/',
    author='Huawei',
    license='Apache License 2.0',
    keywords='huawei cloud development',
    install_requires=install_requires,
    packages=['push_admin'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
    ],
)
