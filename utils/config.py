#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :
@Time    :   2023.07.11
@Desc    :   加载配置文件
"""
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def getConfig(section, option):
    return config.get(section, option)

def getsection(section):
    keys = []
    for key in config.options(section):
        keys.append(config.get(section, key))
    return keys
