import asyncio
from openai import OpenAI
import httpx


import toml
with open('config.toml', 'r') as f:
    config = toml.load(f)
api_key = config["agent4train"]["openai_key"]
base_url = config["agent4train"]["openai_url"]
class Open_AI:
    def __init__(self, api_key,base_url):
        # self.http_client = httpx.AsyncClient()
        self.openai = OpenAI(
            base_url=base_url,
            api_key=api_key,
            # http_client=self.http_client,
        )
        self.api_key = api_key

        self.client = self.openai
    # async def get_completion(self,system_prompt,prompt):
    #     response = await self.client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": system_prompt},
    #             {"role": "user", "content": prompt}
    #         ],
    #         stream=True
    #     )
    #     print(response)
    #     return response
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

    def run_async(self,system_prompt,prompt,messages):
        '''
        在同步环境中运行异步代码.
        '''
        try:
            loop = asyncio.get_event_loop()
        except:
            loop = asyncio.new_event_loop()
        return loop.run_until_complete(self.get_streaming_completion(system_prompt,prompt,messages))

        # 迭代流式响应
        # async for chunk in response:
        #     # chunk 应该是一个字典，直接打印其内容
        #     # print(chunk.choices[0].delta.content)
        #     yield chunk.choices[0].delta.content
        # return

# 运行异步函数以获取流式输出
# async def a():
#     async for i in  get_streaming_completion():
#         if i != None:
#             print(i,end=" ")
# asyncio.run(a())
if __name__ == "__main__":
    oa = OpenAI(api_key,base_url)
    print(oa.get_completion("请简短回答问题","你的问题是什么"))