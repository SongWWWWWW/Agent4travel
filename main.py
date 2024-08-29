import asyncio
import json
import time
from random import uniform
from typing import List, Dict
import requests
import os,sys
sys.path.append(os.path.dirname(__file__))

from agent import  SuperAgent
import streamlit as st
# from openai import OpenAI
from Model.model import Open_AI
import toml
from Model.model import get_openai_stream

config = {}
with open("config.toml",'r') as f:
    config = toml.load(f)



st.title("      Agent for travel")
response = None
# Set OpenAI API key from Streamlit secrets
client = Open_AI(api_key=config["agent4travel"]["openai_key"],base_url=config["agent4travel"]["openai_url"])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

def generator(t:str):
    for i in t:
        yield i
        t = uniform(0,0.1)
        time.sleep(t)
def get_content(stream):
    text = ""

    try:
        for s in stream:
            text += s
        text = json.loads(text)
        print(text)
        if text["策略"] == "用户对话":
            text = text["对话"]
        else:
            text = "正在为您调用工具..."
        return generator(text)
    except Exception as e:
        print("Error parsing main.py",e)
    pass


with st.chat_message("assistant"):
    if prompt != None:
        # print(prompt)
        agent = SuperAgent()
        stream = get_openai_stream(sys_prompt=agent.sys_prompt,prompt=agent.pre_prompt.format(text=prompt.replace("{","{{").replace("}","}}")),messages=st.session_state.messages)
        # stream,
        stream = list(stream)
        s = get_content(stream)
        response = st.write_stream(s)
        print(response)

        if response is not None :
            out = agent.parse_output(stream)
            if out is not None:
                if "<!DOCTYPE html>" in out:
                    st.write("路径规划如下")
                    html_component = st.components.v1.html(out, height=600)
                elif "http" in out:
                    st.image(out,width=600)
                elif isinstance(out,list):
                    s = ""
                    for i in out:
                        s += i + ","
                    response_agent = "景点有"+s[:-1]
                    st.write_stream(generator(response_agent))

    else:
        stream = None

if prompt is not None:
    st.session_state.messages.append({"role": "user", "content": prompt})
if response is not None:
    st.session_state.messages.append({"role": "assistant", "content": response + response_agent})
