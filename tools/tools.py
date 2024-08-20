import json
import traceback
from typing import List, Dict
import requests

from Model.model import get_openai_stream
from baiduAPI import BaiduAPI
import toml
import os,sys
from .calculate_path import find_shortest_path
# print(sys.path)
sys.path.append(os.path.dirname(__file__))
from frontend.html_st import Html
with open('config.toml', 'r') as f:
    config = toml.load(f)
    ak = config["agent4travel"]["ak"]

def multi_path_routing(locations:List[str]):
    # 涉及多个请求
    baidu = BaiduAPI(ak)
    site = []
    distances = {}
    paths = {}
    site.append(i for i in range(len(locations)))
    for i in range(len(locations)):
        for j in range(i+1, len(locations)):
            # distance: List[Tuple[float,float]] , path:
            try:
                path, distance = baidu.multi_parse_path_planing_result(locations[i], locations[j])
            except Exception as e:
                print("Error: ")
                print(locations[i],locations[j])
            paths[(i,j)] = path
            distances[(i,j)] = distance
    shortest_path_list, shortest_path_length = find_shortest_path(distances,len(locations))
    print(shortest_path_list)
    shortest_path = []
    sum_path = []
    for index, i in enumerate(shortest_path_list):
        shortest_path.append(locations[i])
        if index != len(shortest_path_list) - 1:

            if shortest_path_list[index+1] > shortest_path_list[index]:
                p = paths[(shortest_path_list[index], shortest_path_list[index + 1])].copy()
                for i in p:
                    sum_path.append(i)
            else:
                p = paths[(shortest_path_list[index + 1], shortest_path_list[index])].copy()
                p.reverse()
                for i in p:
                    sum_path.append(i)
    lat,lng = baidu.get_address_encode(shortest_path[0])
    return (lng,lat),shortest_path, sum_path




def image_search(location:str):
    url = "http://127.0.0.1:8000/search-images-url/"
    params = {"query": location}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "image_url" in data:
            # print(data["image_url"])
            return data["image_url"]
        else:
            print("Error:", data)
            return None
def scenic_spot_search_parse(result: Dict[str,List[Dict]]):
    try:
        if result["search_results"] != []:
            for r in result["search_results"]:
                if r["full_content"] != "":
                    prompt = f"""
                    请从下面由```包裹的一段话中提取出不包含城市名称的景点名称,景点的名称不应该是常见的名词。
                    回答的形式:

                    1. 用JSON的形式回答，key为position，value为文本提取出的景点名称，类型为List[str]
                    2. 没有找到景点名称时，value为None
                    3. 如果找到景点名称则加入value中，忽略任何城市或地区名称

                    回答请按照以下的示例：
                    {{
                        "position": ["景点A", "景点B"]  # 没有找到则为None
                    }}

                    需要提取旅游景点的文本如下：
                    ```{r["full_content"]}```
                    """

                    response = get_openai_stream("请根据提供的文本按照要求和指定的格式进行输出", prompt,messages=[])
                    text = ""
                    for chunk in response:
                        # print(chunk)
                        text += chunk
                    print(text)
                    text = json.loads(text.strip("```").strip("json"))
                    if len(text["position"]) > 1:
                        return text["position"]
            return []
        else:
            return []
    except Exception as e:
        print("agent: ",e)
        # traceback.print_exc()
        return []
def scenic_spot_search(location:str):

    url = "http://127.0.0.1:8000/search/"
    params = {"keyword": location}
    response = requests.get(url, params=params)
    print("v1",response)
    if response.status_code == 200:
        data = response.json()
        return scenic_spot_search_parse(data)
    return None
tools_dict = {
    "两点路线规划": BaiduAPI(ak).get_html, # 返回html
    "坐标转换": BaiduAPI(ak).transform, # 返回str , 弃用
    "多地点路线规划": multi_path_routing, # 返回html
    "景点图片查询": image_search, # 返回url
    "某地景点查询": scenic_spot_search, # 返回 Dict[List[Dict]] -> 解析为list[str]
}

if __name__ == '__main__':

    # print(tools_dict)
    # fuc = tools_dict["多地点路线规划"]
    # locations = ["山东大学威海","威海国际海水浴场","威海火炬八街"]
    # start, shortest_path, sum_path = multi_path_routing(locations)
    # import streamlit as st
    # with open("../config.toml", "r") as f:
    #     config = toml.load(f)
    #
    # html = Html(ak=config["agent4travel"]["ak"],start=start,path=sum_path)
    # print(html)
    # print(html.html)
    # st.components.v1.html(html.html, height=600)
    print(scenic_spot_search("北京"))