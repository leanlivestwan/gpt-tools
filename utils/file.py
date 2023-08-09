#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :
@Time    :   2023.07.11
@Desc    :   读写数据文件
"""
import os
import pandas as pd
import utils.config as config


DEFALT_INPUT = os.getcwd() + config.getConfig(f"data", "input")
DEFALT_OUTPUT = os.getcwd() + config.getConfig(f"data", "output")


def load_csv(path=DEFALT_INPUT):
    csvframe = pd.read_csv(path)
    return csvframe


def save_csv(csv: pd.DataFrame, path=DEFALT_OUTPUT):
    if os.path.exists(path):
        os.remove(path)
    csv.to_csv(path, index=False)
    return
