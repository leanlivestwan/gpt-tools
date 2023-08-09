#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :
@Time    :   2023.07.19
@Desc    :   GPT请求公共方法
"""
import openai
import utils.config as config
import time

MAX_REQUEST_INTERVAL = 60 / 20  # 60s  20个

api_key = config.getConfig("gpt.key", "key0")
api_base = config.getConfig("gpt.api", "url")

if not api_key:
    raise ValueError("缺少参数：gpt.key，请检查配置文件")
if not api_base:
    raise ValueError("缺少参数：gpt.api，请检查配置文件")

# openai.log = "debug"
openai.api_key = api_key
openai.api_base = api_base


def gpt_35_polish(messages: list, gpt_key):
    openai.api_key = gpt_key.name
    # print(gpt_key.cur_time, gpt_key.last_time, gpt_key.index)
    if gpt_key.cur_time - gpt_key.last_time < MAX_REQUEST_INTERVAL:
        time.sleep(MAX_REQUEST_INTERVAL - (gpt_key.cur_time - gpt_key.last_time))
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
            temperature=0.2,
            max_tokens=5000,
            presence_penalty=1,
        )
        completion = {"role": "", "content": ""}
        for event in response:
            if event["choices"][0]["finish_reason"] == "stop":
                # print(f'收到的完成数据: {completion}')
                break
            for delta_k, delta_v in event["choices"][0]["delta"].items():
                # print(f'流响应数据: {delta_k} = {delta_v}')
                completion[delta_k] += delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        return (True, messages, gpt_key.index)
    except Exception as err:
        print(f"OpenAI API 异常:{err}", gpt_key.index)
        return (False, messages, gpt_key.index)
