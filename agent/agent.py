#!/usr/bin/env python3

import json
import traceback
from typing import Generator, Union, Dict, List

import requests

from prompt import ControllerPrompt,DialogPrompt, SuperPrompt
from tools.tools import tools_dict
from Model.model import get_openai_stream
import os,sys
sys.path.append(os.path.dirname(__file__))
class BaseAgent:
    def __init__(self):
        pass
    def parse_output(self):
        pass


class ControllAgent(BaseAgent,ControllerPrompt):
    def __init__(self):
        super().__init__()

class DialogAgent(BaseAgent,DialogPrompt):
    def __init__(self):
        super(BaseAgent,self).__init__()
    def parse_output(self,output:str):
        args=[]
        func = None
        positions = []
        for k,v in tools_dict.items():
            if k in output:
                func = tools_dict[k]
        if not func:
            return False
        for index, i in enumerate(output):
            if i == "\"":
                positions.append(index)
        try:
            for index in range(0,len(positions),2):

                print(output[positions[index]:positions[index+1]].strip("\""))
                args.append(output[positions[index]:positions[index+1]].strip("\""))
        except Exception as e:
            print("输出的\"的数量有问题")
        if len(args) == 0:
            return False
        return func(*args)

class SuperAgent(BaseAgent,SuperPrompt):
    def __init__(self):
        super(SuperPrompt,self).__init__()
        super(BaseAgent,self).__init__()


    def parse_output(self,output:Union[list,str]):
        fuc = None
        tools_select = None
        if isinstance(output, list):
            text = ""
            for i in output:
                text += i
            output = text
        try:
            # 先解析第一部分的输出
            out = json.loads(output)
            if out["策略"] == "工具调用":
                print("工具调用")
                fuc = tools_dict[out["工具"]]
            # 解析第二部分输出
            if fuc:
                tool = get_openai_stream(self.tools_sys_prompt,self.tools_prompt.format(text=out["工具输入"]),messages=[])
                text = ""
                for chunk in tool:
                    # print(chunk)
                    text += chunk
                tools_select = json.loads(text)
                print(tools_select)
                args = tools_select["args"]
                print("工具参数: ", args)
                return fuc(*args)
            return None
        except Exception as e:
            print("解析错误")
            if tools_select is not None:
                print(tools_select)
            print("agent",e)



if __name__ == "__main__":
    import streamlit as st
    # agent = DialogAgent()
    # html_temp = agent.parse_output("路线规划(\"哈尔滨工业大学威海\",\"山东大学威海\")")
    # html_component = st.components.v1.html(html_temp, height=600)
    #
    # # 显示经纬度
    # if html_component:
    #     st.write(f"点击位置经纬度: {html_component}")
    agent = SuperAgent()
    # print(agent.sys_prompt)
    # print(agent.pre_prompt)
    result = requests.get("http://127.0.0.1:8000/search/?keyword=大连")

    print(agent.scenic_spot_search(json.loads(result.text)))