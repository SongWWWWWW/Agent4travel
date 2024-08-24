import base64
import json
from http.client import HTTPException
from typing import List

import requests
import toml
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import StreamingResponse

from baiduAPI import BaiduAPI
from Model.model import  Open_AI
import toml
from pydantic import BaseModel,Field
from auto_gptq import AutoGPTQForCausalLM
from transformers import LlamaTokenizer
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
# openai = Open_AI(api_key, base_url)
# 用yuan
path = '/root/autodl-fs/YuanLLM/Yuan2-M32-HF-INT4'

print("Creat tokenizer...")
tokenizer = LlamaTokenizer.from_pretrained(path, add_eos_token=False, add_bos_token=False, eos_token='<eod>')
tokenizer.add_tokens(['<sep>', '<pad>', '<mask>', '<predict>', '<FIM_SUFFIX>', '<FIM_PREFIX>', '<FIM_MIDDLE>','<commit_before>','<commit_msg>','<commit_after>','<jupyter_start>','<jupyter_text>','<jupyter_code>','<jupyter_output>','<empty_output>'], special_tokens=True)

print("Creat model...")
model = AutoGPTQForCausalLM.from_quantized(path, trust_remote_code=True).cuda()

# 允许所有来源访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def bing_image_search(query: str):
    url = 'https://www.bing.com/images/search'
    params = {'q': query}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return {'error': '检索图像失败，请检查网络'}, None

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('img', class_='mimg')

    if img_tag is None:
        return {'error': '未找到相关图像'}, None

    img_url = img_tag['src']
    if img_url.startswith('data:image/'):
        image_data = img_url.split(',')[1]
        return None, base64.b64decode(image_data)
    else:
        return None, img_url

def bing_search(keyword, num_results=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    params = {
        'q': f"{keyword}附近景点",
        'count': num_results
    }
    print(params)
    url = 'https://cn.bing.com/search'
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.select('li.b_algo'):
        try:
            title = item.h2.get_text(strip=True)
            link = item.h2.a['href']
            snippet = item.p.get_text(strip=True) if item.p else ''
            full_content = get_full_content(link)
            results.append({'title': title, 'link': link, 'snippet': snippet, 'full_content': full_content})
        except (AttributeError, KeyError):
            continue

    return results
def get_full_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content = '\n'.join([p.get_text(strip=True) for p in soup.find_all('p')])
        if content:
            return content
        else:
            # 如果找不到，尝试其他选择器或者返回空字符串
            return ''
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ''

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
        #stream = openai.get_streaming_completion(request.sys_prompt,request.prompt,request.messages)
        # 用yuan
        prompt = request.sys_prompt + request.prompt
        prompt += "<sep>"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, do_sample=False, max_new_tokens=256)
        output = tokenizer.decode(outputs[0])
        response = output.split("<sep>")[-1]
        def generate():
            for chunk in response.split(" "):
                yield chunk
        # 将流对象转换为可以用于StreamingResponse的生成器
        # def generate():
        #     for chunk in stream:
        #         # yield chunk
        #         if chunk.choices[0].delta.content:
        #             print(chunk)
        #             # 直接返回内容str，去除其他无用的数据，便于encode和decode的处理
        #             yield chunk.choices[0].delta.content
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


@app.get("/search-images/")
async def search_images(query: str):
    error, image_data_or_url = bing_image_search(query)
    if error:
        return error
    if isinstance(image_data_or_url, bytes):
        return StreamingResponse(content=iter([image_data_or_url]), media_type='image/jpeg')
    else:
        # 直接从URL返回图像数据
        image_response = requests.get(image_data_or_url, stream=True)
        return StreamingResponse(content=image_response.raw, media_type='image/jpeg')

@app.get("/search-images-url/")
async def search_images_url(query: str):
    """
    Search for images using Bing's image search API and return the image URL.

    Parameters:
    -----------
    query : str
        The search term or keyword to use for finding images.

    Returns:
    -----------
    dict
        A dictionary containing the image URL if the search is successful. If an error occurs, returns an error message.

    Example:
    -----------
    >>> import requests
    >>> url = "http://127.0.0.1:8000/search-images-url/"
    >>> params = {"query": "sunrise"}
    >>> response = requests.get(url, params=params)
    >>> if response.status_code == 200:
    ...     data = response.json()
    ...     if "image_url" in data:
    ...         print(data["image_url"])
    ...     else:
    ...         print("Error:", data)

    Notes:
    -----------
    - This function calls the `bing_image_search` utility, which interacts with Bing's API.
    - The function first checks if an error occurred during the search.
    - If the search is successful and the result is a string, it assumes it's the URL of the image.
    - The response is a JSON object with the image URL, or an error message if something goes wrong.
    """
    error, image_data_or_url = bing_image_search(query)
    if error:
        return error
    if isinstance(image_data_or_url, str):
        return {'image_url': image_data_or_url}

@app.get("/search/")
async def search(keyword: str):
    """
    Perform a web search using Bing's search API and return the search results.

    Parameters:
    -----------
    keyword : str
        The search term or query string used to find relevant web pages.

    Returns:
    -----------
    dict
        A dictionary containing a list of search results obtained from Bing.

    Example:
    -----------
    >>> import requests
    >>> url = "http://127.0.0.1:8000/search/"
    >>> params = {"keyword": "python programming"}
    >>> response = requests.get(url, params=params)
    >>> if response.status_code == 200:
    ...     data = response.json()
    ...     print(data)

    Notes:
    -----------
    - This function interacts with the `bing_search` utility to fetch search results from Bing's API.
    - The results are returned as a JSON object containing a list of search results.
    - The response is straightforward, consisting of the search results or an empty list if no results are found.
    """
    search_results = bing_search(keyword)
    return {'search_results': search_results}




if __name__ == "__main__":
    # 为什么要将所有的模型的调用放置在后端统一管理？
    # 1. 便于监测token的使用量和token的使用分布
    # 2. 便于维护和更新
    uvicorn.run("api:app", host="localhost", port=8000)