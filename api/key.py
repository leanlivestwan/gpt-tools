#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :
@Time    :   2023.07.19
@Desc    :   获取gpt所有keys
"""

import time
import utils.config as config

class gpt_key_time_mgt:
    last_time = 0
    cur_time = 0
    name = ""
    index = 0
    status = False

def get_gpt_keys():
    gpt_key_names = config.getsection(f"gpt.key")  # 获取所有gpt keys
    gpt_keys = []
    for key_ind in range(len(gpt_key_names)):
        gpt_key_obj = gpt_key_time_mgt()
        gpt_key_obj.last_time = 0
        gpt_key_obj.cur_time = time.time()
        gpt_key_obj.name = gpt_key_names[key_ind]
        gpt_key_obj.index = key_ind
        gpt_key_obj.status = True
        gpt_keys.append(gpt_key_obj)
    print("成功获取到gpt key数量: ", len(gpt_keys))
    return gpt_keys