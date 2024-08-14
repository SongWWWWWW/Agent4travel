import asyncio
import json
from typing import List, Dict

from openai import OpenAI
import toml
import os,sys
sys.path.append(os.path.dirname(__file__))
import requests
def get_openai_stream(sys_prompt:str,prompt:str,messages:List[Dict]):
    """
    transform the StreamingResponse to a generator and decode all chunks
    """
    try:
        payload = {
            "sys_prompt": sys_prompt,
            "prompt": prompt,
            "messages": messages
        }
        # print(json.dumps(payload))
        response = requests.post("http://127.0.0.1:8000/openai", data=json.dumps(payload), stream=True)
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                # print(chunk)
                yield chunk
    except Exception as e:
        print("main.py get_stream error",e)
class Open_AI:
    def __init__(self, api_key,base_url):

        self.openai = OpenAI(
            base_url=base_url,
            api_key=api_key,
            # http_client=self.http_client,
        )
        self.api_key = api_key
        self.client = self.openai

    def get_streaming_completion(self,system_prompt,prompt,messages):
        # 调用 chat.completions.create 并启用流式输出
        message_list = messages + [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_list,
            stream=True  # 启用流式输出
        )
        return response

if __name__ == "__main__":
    pass
    # oa = Open_AI(api_key,base_url)
    # print(oa.get_streaming_completion("请简短回答问题","你的问题是什么",[]))