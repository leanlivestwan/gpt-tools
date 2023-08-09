#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :
@Time    :   2023.07.19
@Desc    :   基于GPT的多线程任务处理
"""
import time
import pandas as pd

import utils.file as file
import concurrent.futures
import api.key as key
import server.polish_server as server_pool

# 全局变量
THREAD_NUM = 10  # 线程池中线程数量
MAX_REQUEST_NUM = 10  # 控制所有gpt_key的最大并发数量，理论值 = max_num * len(gpt_keys)
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_NUM)


if __name__ == "__main__":
    # 不同的任务切换不同的server即可
    server = server_pool.FAQPolishServer()
    inputFrame = server.load_data()

    if inputFrame.empty:
        raise ValueError("输入数据为空，任务已退出，请检查输入路径或输入文件是否正确。")

    print(f"开始执行任务: {server.descript}，任务数量{len(inputFrame)}")
    outputFrame = server.get_df()
    gpt_keys = key.get_gpt_keys()

    idx = 0
    gpt_key_index = 0
    future_list = []
    for row in inputFrame.itertuples():
        if len(future_list) >= MAX_REQUEST_NUM:
            concurrent.futures.wait(
                future_list, return_when=concurrent.futures.FIRST_COMPLETED
            )
            remainder = []
            for f in future_list:
                if f.done():
                    result = f.result()
                    gpt_keys[result[2]].last_time = gpt_keys[result[2]].cur_time
                    gpt_keys[result[2]].status = True
                    outputFrame = pd.concat([outputFrame, result[1]], ignore_index=True)
                else:
                    remainder.append(f)
            future_list = remainder
        promptBase = server.get_prompt(row)
        messages = [
            {"role": "assistant", "content": promptBase},
        ]
        while not gpt_keys[gpt_key_index].status:
            gpt_key_index = (gpt_key_index + 1) % len(gpt_keys)
            time.sleep(0.001)

        gpt_keys[gpt_key_index].status = False
        gpt_keys[gpt_key_index].cur_time = time.time()
        future = thread_pool.submit(
            server.run, row, messages, gpt_keys[gpt_key_index]
        )  # 线程池方法
        future_list.append(future)
        gpt_key_index = (gpt_key_index + 1) % len(gpt_keys)
        print("当前开始处理任务：", idx)
        idx += 1
        # for debug
        if idx >= 5:
            break

    concurrent.futures.wait(future_list)
    # 处理future_list中剩余的数据
    for f in future_list:
        if f.done():
            result = f.result()
            gpt_keys[result[2]].last_time = gpt_keys[result[2]].cur_time
            outputFrame = pd.concat([outputFrame, result[1]], ignore_index=True)
    print("任务结束")
    file.save_csv(outputFrame)
