#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :
@Time    :   2023.07.19
@Desc    :   基于GPT润色server
"""
import os
import jsonlines
import pandas as pd

import utils.config as config
import utils.file as file
from api.gpt import gpt_35_polish as model


class FAQPolishServer:
    descript = "基于GPT进行FAQ润色"

    def load_data(self):
        return file.load_csv()

    def get_df(self):
        return pd.DataFrame(columns=["question", "origin_answer", "polish_answer"])

    def get_prompt(self, row):
        question = getattr(row, "question")
        answer = getattr(row, "answer")
        prompt = f"""
        假如你是一名安全书籍的编辑，现在你需要完成一本安全百科的文字润色工作，你会得到一个问题和一个回答，你需要根据问题把当前回答进行润色，可以通过增加背景描述、调整句子顺序与结构等方式，让回答变得更加完整通顺并且方便人类理解，请尽可能地让回答变的更加丰富，内容更加多一些。
        问题：{question}
        回答：{answer}
        请用中文直接输出润色后的回答，不需要带有“回答：”这种开头。
        """
        return prompt

    def run(self, row, messages, gpt_key):
        question = getattr(row, "question")
        answer = getattr(row, "answer")
        (status, response, index) = model(messages, gpt_key)
        if not status or len(response) < 2 or response[1]["role"] != "assistant":
            appendFrame = pd.DataFrame(
                {
                    "question": question,
                    "origin_answer": answer,
                    "polish_answer": -1,
                },
                index=[0],
            )
            print("assistent error")
            return (False, appendFrame, index)
        gpt_res = response[1]["content"]
        appendFrame = pd.DataFrame(
            {
                "question": question,
                "origin_answer": answer,
                "polish_answer": gpt_res,
            },
            index=[0],
        )
        print(appendFrame)
        return (True, appendFrame, index)


class eventAnalysisPolishServer:
    descript = "基于GPT进行文字润色"

    def load_data(self):
        return file.load_csv()

    def get_df(self):
        return pd.DataFrame(columns=["task_name", "origin_answer", "polish_answer"])

    def get_prompt(self, row):
        task_name = getattr(row, "task_name")
        answer = getattr(row, "question")
        prompt = f"""
        假如你是一名安全报告的编辑，现在你需要完成一起安全相关事件解读报告的文字润色工作，你会得到一个安全相关事件的详细描述，你需要根据安全相关事件对报告进行润色，可以通过调整句子顺序与结构等方式，让回答变得更加完整通顺并且方便人类理解。
        报告：{task_name}
        回答：{answer}
        请用中文直接输出润色后的回答，不需要带有“回答：”这种开头。
        """
        return prompt

    def run(self, row, messages, gpt_key):
        task_name = getattr(row, "task_name")
        answer = getattr(row, "question")
        (status, response, index) = model(messages, gpt_key)
        if len(response) < 2 or response[1]["role"] != "assistant":
            appendFrame = pd.DataFrame()
            print("assistent error")
            return appendFrame
        gpt_res = response[1]["content"]
        appendFrame = pd.DataFrame(
            {
                "task_name": task_name,
                "origin_answer": answer,
                "polish_answer": gpt_res,
            },
            index=[0],
        )
        print(appendFrame)
        return (True, appendFrame, gpt_key.index)


class securityEncyclopediaPolishServer:
    descript = "基于GPT进行安全百科润色"

    def load_data(self):
        path = os.getcwd() + config.getConfig(f"data", "input")
        dict_all = []
        with open(path) as f:
            for item in jsonlines.Reader(f):
                conversations = item.get("conversations")
                dict_single = {}
                if len(conversations) < 2:
                    continue
                for line in conversations:
                    key = line.get("from")
                    value = line.get("value")
                    if key == "human":
                        dict_single.setdefault("question", value)
                    elif key == "gpt":
                        dict_single.setdefault("answer", value)
                dict_all.append(dict_single)
        inputFrame = pd.DataFrame(dict_all)
        return inputFrame

    def get_df(self):
        return pd.DataFrame(columns=["question", "origin_answer", "polish_answer"])

    def get_prompt(self, row):
        question = getattr(row, "question")
        origin_answer = getattr(row, "answer")
        prompt = f"""
        假如你是一名安全书籍的编辑，现在你需要完成一本安全百科的文字润色工作，你会得到一个问题和一个回答，你需要根据问题把当前回答进行润色，可以通过增加背景描述、调整句子顺序与结构等方式，让回答变得更加完整通顺并且方便人类理解。
        问题：{question}
        回答：{origin_answer}
        请用中文直接输出润色后的回答，不需要带有“回答：”这种开头。
        """
        return prompt

    def run(self, row, messages, gpt_key):
        question = getattr(row, "question")
        origin_answer = getattr(row, "answer")
        (status, response, index) = model(messages, gpt_key)
        if len(response) < 2 or response[1]["role"] != "assistant":
            appendFrame = pd.DataFrame()
            print("assistent error")
            return appendFrame
        gpt_res = response[1]["content"]
        appendFrame = pd.DataFrame(
            {
                "question": question,
                "origin_answer": origin_answer,
                "polish_answer": gpt_res,
            },
            index=[0],
        )
        print(appendFrame)
        return (True, appendFrame, gpt_key.index)
