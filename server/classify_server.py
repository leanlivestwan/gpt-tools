#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :
@Time    :   2023.07.19
@Desc    :   基于GPT进行API分类
"""
import os
import pandas as pd

import utils.file as file
from api.gpt import gpt_35_polish as model


class classifyServer:
    descript = "基于GPT进行API多分类"

    def load_data(self):
        return file.load_csv()

    def get_df(self):
        return pd.DataFrame(
            columns=["question", "origin_api", "gpt_api", "gpt_evidence", "consistency"]
        )

    def get_prompt(self, row):
        question = getattr(row, "content")
        prompt = f"""
        假如你是一名安全运维人员，你需要仔细理解客户提出的的问题，并判断该问题是否有必要查询对应的API获取关键数据来回复客户。
        要求1：你需要注意区分analyze和get类型的API功能区别，如果客户的问题是要求解读分析，优先调用analyze的API。
        要求2：不需要调用API的问题，目标API为other。
        数据格式说明：以incident为开头的字符数字组合是事件的唯一id，以alert为开头的字符数字组合是告警的唯一id。

        现在有以下API详情说明，请注意有些API侧重于内容获取，有些API提供解读分析的功能：
        getIncidentList:获取安全事件的详细信息，可选指定时间范围、严重等级、主机IP、事件名称或威胁类型名称零个或多个条件
        getIncidentAgg:获取安全事件的统计聚合信息。可支持筛选限定条件后再进行聚合。支持聚合字段：主机IP, 事件处置状态, 事件严重等级, 事件名
        getIncidentTrend:获取一段时间内的安全事件趋势，例如数量变化，可支持指定时间范围
        analyzeIncident:解读分析安全事件，包括事件描述、攻击时间线过程、处置建议等
        getPayload:获取网络侧事件或告警的攻击数据包原文
        analyzePayload:分析解读网络侧事件或告警的攻击数据包，包括payload中的攻击意图、攻击来源、攻击方法等
        getAttackTrend:获取一段时间的安全趋势，包括安全事件发展趋势、安全告警发展趋势、资产概览，以及相应的各个趋势发展图
        getAlertList:获取安全告警的详细信息，包括攻击行为、威胁、病毒、漏洞攻击、异常流量等，可选指定时间范围、源IP、目的IP、攻击威胁类型、严重等级零个或多个条件
        getAlertAggregation:获取安全告警的统计聚合信息，包括攻击行为、威胁、病毒、漏洞攻击、异常流量等，支持聚合字段：告警名称、告警等级、可信度、告警类型、源IP、目的IP、资产主机IP、攻击结果、处置状态、告警来源
        getVulTop5:获取公司内的资产中存在漏洞或弱密码问题最多的资产topN
        getRiskAppTop10:获取公司内的资产中存在最多的风险应用程序topN，支持指定特定的主机IP
        getHotVul:获取业界最近的热点漏洞，非公司内部资产的漏洞
        getVulTrend:获取公司内资产存在的热点漏洞列表
        getDNSLog:指定源IP、域名信息，查询一段时间内的DNS域名访问、请求记录
        getHTTPLog:指定源IP、访问的url部分链接，查询一段时间内的HTTP访问记录
        getIPLog:指定源IP、目的IP、目的端口，查询一段时间内的网络连接五元组信息记录
        getEndpointProcess:指定进程名、进程路径、进程MD5、进程执行命令行，查询终端主机的进程创建记录
        getEndpointFile:指定文件名、文件路径、文件hash，查询终端主机的文件创建、文件修改、文件重命名、文件删除记录
        getEndpointNet:指定五元组信息，查询终端主机的五元组信息
        getEndpointDNS:指定域名信息，查询终端主机的域名访问信息
        getEndpointService:指定服务名、服务状态，查询终端主机的服务信息
        getEndpointAccount:指定账号名、账户操作IP，查询终端主机的账户创建、账户删除信息
        getEndpointLogin:指定登录用户、登录IP，查询终端主机的登录信息
        getAssetPortTop5:获取公司内的资产中使用最多的端口topN
        getApplicationTop5:获取公司内的资产中使用最多的软件、应用程序topN
        getRiskAssetRank:获取风险资产分布情况
        getRiskAssetTend:获取风险资产变化趋势
        getAssetListByDev:指定设备名称，查询来源于该设备的资产详细列表信息
        getVulInfo:获取公司内的资产中存在的漏洞信息，支持以主机进行聚合。支持指定修复状态、修复优先级、漏洞名、漏洞等级、漏洞类型（高可利用、活跃漏洞、热点漏洞、病毒利用、有攻击代码披露）、主机IP等进行查询
        getWeakPWDInfo:获取公司内的资产中存在的弱密码/弱口令情况，支持以主机进行聚合。支持指定是否为管理员账号、内外网信息、登录状态、服务类型、处置状态、弱密码类型、主机IP等进行查询
        getEventInfo:获取一段时间内的事件处置情况，支持指定时间类型、主机IP、处置状态、风险等级、服务类型进行查询
        getNSecurityLogInfo:获取一段时间内的网络流量安全日志信息，支持指定攻击方向、主机IP进行查询
        getAssetInfo:获取资产的详细信息，支持指定资产名称、责任人、资产分组、资产类型、操作系统类型、接入状态、端口、应用程序、服务、计划任务、是否为核心资产等进行查询
        getAssetAgg:获取资产相关的统计聚合信息，当前支持的聚合对象包括：资产类型、操作系统、端口、应用程序、服务、接入状态

        客户的问题是：{question}

        请先回答是否需要调用API，如果不需要，请回答不需要，如果需要，在只能查询一个API的条件下给出目标API，并给出调用该API的理由，理由主要包含以下内容：客户的问题意图描述，目标API功能描述，API功能与用户意图是否匹配;

        请按照以下格式完成输出：
        目标API: XXX
        理由: XXX
        """
        return prompt

    def run(self, row, messages, gpt_key):
        origin_api = getattr(row, "label")
        origin_question = getattr(row, "content")
        response = model(messages, gpt_key)
        if len(response) < 2 or response[1]["role"] != "assistant":
            appendFrame = pd.DataFrame()
            print("assistent error")
            return appendFrame
        gpt_res = response[1]["content"]
        if "目标API" not in gpt_res or "理由" not in gpt_res:
            appendFrame = pd.DataFrame()
            return appendFrame
        gpt_api = gpt_res.split("目标API:")[1].split("理由")[0].replace("\n", "").strip()
        gpt_evidence = gpt_res.split("理由:")[1].replace("\n", "").strip()
        consistency = 1 if gpt_api in origin_api else 0
        appendFrame = pd.DataFrame(
            {
                "question": origin_question,
                "origin_api": origin_api,
                "gpt_api": gpt_api,
                "gpt_evidence": gpt_evidence,
                "consistency": consistency,
            },
            index=[0],
        )
        print(appendFrame)
        return (True, appendFrame, gpt_key.index)
