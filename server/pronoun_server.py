#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :
@Time    :   2023.07.19
@Desc    :   基于GPT泛化指代词
"""
import json
from ast import literal_eval
import pandas as pd

import utils.file as file
from api.gpt import gpt_35_polish as model


class SecurityPronounServer:
    descript = "基于GPT泛化指代词"

    def load_data(self):
        return file.load_csv()

    def get_df(self):
        return pd.DataFrame(columns=["question", "answer", "sentence", "rewrite"])

    def get_prompt(self, row):
        question = getattr(row, "question")
        answer = getattr(row, "answer")
        prompt = f"""
        请你现在扮演一个网络安全领域的专家，你需要根据你的专业知识帮我对以下问题和回答进行二次提问
        ```
        问题：{question}
        回答：{answer}
        ```
        二次提问中需要包含指代词，包括但不限于"这些"、"那个"、"最后一个"、"最早的"、"这几个"等指代词，在不改变语义顺序的情况下，基于指代词对二次提问的问题进行指代消解，替换成问题或回答中的实体对象，得到指代消解后的问题内容。
        举例：
        ```
        {{"二次提问":"最后一个资产的漏洞数是多少？","指代消解后的问题内容":"统计航港发展有限公司的资产10.200.32.175的漏洞数是多少？"}}
        ```
        请你提供3个版本用于参考,不需要解释,以下面的json格式依次输出
        ```
        [
        {{"二次提问":"","指代消解后的问题内容":""}},
        {{"二次提问":"","指代消解后的问题内容":""}},
        {{"二次提问":"","指代消解后的问题内容":""}},
        ...
        ]
        ```
        """

        return prompt

    def run(self, row, messages, gpt_key):
        question = getattr(row, "question")
        answer = getattr(row, "answer")
        (status, response, index) = model(messages, gpt_key)
        responseFrame = pd.DataFrame(
            columns=["question", "answer", "sentence", "rewrite"]
        )
        if not status or len(response) < 2 or response[1]["role"] != "assistant":
            appendFrame = pd.DataFrame(
                {
                    "question": question,
                    "answer": answer,
                    "sentence": -1,
                    "rewrite": -1,
                },
                index=[0],
            )
            print("assistent error")
            return (False, appendFrame, index)
        gpt_res = response[1]["content"]
        try:
            gpt_rest_list = literal_eval(gpt_res)
        except SyntaxError:
            print("未知错误")
            appendFrame = pd.DataFrame(
                {
                    "question": question,
                    "answer": answer,
                    "sentence": -1,
                    "rewrite": -1,
                },
                index=[0],
            )
            return (False, appendFrame, index)
        if isinstance(gpt_rest_list, list):
            for item in gpt_rest_list:
                sentence = item["二次提问"]
                rewrite = item["指代消解后的问题内容"]
                appendFrame = pd.DataFrame(
                    {
                        "question": question,
                        "answer": answer,
                        "sentence": sentence,
                        "rewrite": rewrite,
                    },
                    index=[0],
                )
                print(appendFrame)
                responseFrame = pd.concat(
                    [responseFrame, appendFrame], ignore_index=True
                )

        return (True, responseFrame, index)
