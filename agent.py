# from builtins import function
from typing import List, Tuple

from prompt import ControllerPrompt,DialogPrompt
from tools import  tools_dict

class BaseAgent:
    def __init__(self):
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


if __name__ == "__main__":
    import streamlit as st
    agent = DialogAgent()
    html_temp = agent.parse_output("路线规划(\"哈尔滨工业大学威海\",\"山东大学威海\")")
    html_component = st.components.v1.html(html_temp, height=600)

    # 显示经纬度
    if html_component:
        st.write(f"点击位置经纬度: {html_component}")

