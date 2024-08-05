import asyncio
from agent import DialogAgent
import streamlit as st
# from openai import OpenAI
from model import Open_AI
def run_async(cor):
    '''
    在同步环境中运行异步代码.
    '''
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
    return loop.run_until_complete(cor)


def iter_over_async(ait, loop=None):
    '''
    将异步生成器封装成同步生成器.
    '''
    ait = ait.__aiter__()

    async def get_next():
        try:
            obj = await ait.__anext__()
            return False, obj
        except StopAsyncIteration:
            return True, None

    if loop is None:
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()

    while True:
        done, obj = loop.run_until_complete(get_next())
        if done:
            break
        yield obj
st.title("      Agent for train")
response = None
# Set OpenAI API key from Streamlit secrets
import toml
config = {}
with open("config.toml",'r') as f:
    config = toml.load(f)
# print(config["agent4train"]["openai_key"])

client = Open_AI(api_key=config["agent4train"]["openai_key"],base_url=config["agent4train"]["openai_url"])

# Set a default model
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

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

with st.chat_message("assistant"):
    if prompt != None:
        agent = DialogAgent()

        stream = client.get_streaming_completion(system_prompt=agent.sys_prompt,prompt=agent.pre_prompt+"\n"+prompt,messages=st.session_state.messages)
        response = st.write_stream(stream)

        if response is not None:
            print(response)
            out = agent.parse_output(response)
            if out:
                st.write("路径规划如下")

                html_component = st.components.v1.html(out, height=600)
    else:
        stream = None

if prompt is not None:
    st.session_state.messages.append({"role": "user", "content": prompt})
if response is not None:
    st.session_state.messages.append({"role": "assistant", "content": response})
