# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : setup.py.py
# Time       ：2022.8.30 23:53
# Author     ：小派精灵
# HomePage   : xiaopy.cn
# Email      : 3383716176@qq.com
# Description：
"""

from setuptools import setup, find_packages
# python setup.py sdist bdist_wheel

setup(
    name='PyGameAutoAndroid',
    version='0.0.12',
    packages=find_packages(),
    license='MIT',
    author='小派精灵',
    author_email='3383716176@qq.com',
    description='小派精灵手机自动化',
    # zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)

