from http.client import HTTPException
from typing import List

import toml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import StreamingResponse

from baiduAPI import BaiduAPI
from Model.model import  Open_AI
import toml
from pydantic import BaseModel,Field
class Message(BaseModel):
    role: str
    content: str
class StreamModel(BaseModel):
    sys_prompt: str
    prompt: str
    messages: List[Message] = Field(default_factory=list,examples=[{"role": "user", "content": "你好，你能帮助我吗？"}])

with open('../config.toml', 'r') as f:
    config = toml.load(f)
    ak = config["agent4travel"]["ak"]
    api_key = config["agent4travel"]["openai_key"]
    base_url = config["agent4travel"]["openai_url"]


app = FastAPI()
baidu = BaiduAPI(ak)
openai = Open_AI(api_key, base_url)

# 允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def test():
    """
    test fastapi

    Example:
    -----------
    >>> import requests
    >>> response = requests.get("http://127.0.0.1:8000/")
    >>> print(response.text)
    """
    return "hello"

@app.get("/baidu/get_path_html")
def get_path_html(start:str,end:str):
    """
    get the html of  the path from start to end using baidu map API

    Parameters：
    -----------
    start ： str
        the beginning of the path
    end : str
        the ending of the path

    Return:
    -----------
    str
        a html about baidu map that can dynamic show the path
    Example:
    -----------
    >>> import requests
    >>> params = {
    ... 'start': start_value,
    ... 'end': end_value
    ... }
    >>> response = requests.get("http://127.0.0.1:8000/baidu/get_path_html",params=params)
    >>> print(response.text)
    """
    with open("../config.toml","r") as f:
        config = toml.load(f)
    browser_ak = config["agent4train"]["browser_ak"]
    html = baidu.get_html(start,end,browser_ak)
    return html

@app.get("/baidu/transforme")
def get_transforme(address:str):
    """
    get the position encoding of address using baidu map API

    Parameters：
    -----------
    address :   str
        the address to get the position encoding
    Return:
    -----------
    str
        concat lat , "," and lng. address's position encoding is (lat,lng)
    Example:
    -----------
    >>> import requests
    >>> params = {
    ... 'start': start_value,
    ... 'end': end_value
    ... }
    >>> response = requests.get("http://127.0.0.1:8000/baidu/get_path_html",params=params)
    >>> print(response.text)
    """
    position = baidu.transform(address)
    print(position)
    return position

@app.post("/openai")
async def chat_completion(request: StreamModel):
    """
    transform the Stream[ChatCompletion] of openai into a StreamingResponse

    Parameters：
    -----------
    request :   StreamModel
        a DataModel includes sys_prompt(str), prompt(str) and messages(List[Message])
        Messages includes role(str), content(str)

    Return:
    -----------
    StreamingResponse
        wrapping a generator from the Stream[ChatCompletion] of openai

    Example:
    -----------
    >>> import requests
    >>> import json
    >>> url = "http://127.0.0.1:8000/openai"
    >>> data = {
    ...     "sys_prompt": "系统提示",
    ...     "prompt": "用户提示",
    ...     "messages": [
    ...         {"role": "user", "content": "你好，你能帮助我吗？"}
    ...     ]
    ... }
    >>> headers = {"Content-Type": "application/json"}
    >>> response = requests.post(url, headers=headers, data=json.dumps(data), stream=True, timeout=10)
    >>> if response.status_code == 200:
    ...     for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    ...         if chunk:
    ...             print(chunk)
    """
    try:
        stream = openai.get_streaming_completion(request.sys_prompt,request.prompt,request.messages)
        # 将流对象转换为可以用于StreamingResponse的生成器
        def generate():
            for chunk in stream:
                # yield chunk
                if chunk.choices[0].delta.content:
                    print(chunk)
                    # 直接返回内容str，去除其他无用的数据，便于encode和decode的处理
                    yield chunk.choices[0].delta.content
        response = StreamingResponse(generate(), media_type="text/event-stream")
        # 设置额外的响应头
        response.headers["Cache-Control"] = "no-cache"  # 禁用缓存
        return response
    except HTTPException as e:
        # Reraise HTTPExceptions to handle specific error cases
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    # 为什么要将所有的模型的调用放置在后端统一管理？
    # 1. 便于监测token的使用量和token的使用分布
    # 2. 便于维护和更新
    uvicorn.run("api:app", host="localhost", port=8000)