from typing import Dict, List, Tuple
import os,sys
sys.path.append(os.path.dirname(__file__))
# import folium
import requests
# from streamlit_folium import st_folium
from html_st import Html
from sdata import  SData
import toml
with open('config.toml', 'r') as f:
    config = toml.load(f)
ak = config['agent4train']['ak']


def transform(ak, address):
    s, e = BaiduAPI(ak).get_address_encode(address)
    result = str(s) + "," + str(e)
    return result

class BaiduAPI:
    def __init__(self, ak):
        self.ak = ak

    def get_address_encode(self, address):
        url = 'http://api.map.baidu.com/geocoding/v3/'
        params = {
            'address': address,
            'output': 'json',
            'ak': ak
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            result = response.json()
            # 打印结果
            print(result)
            # 提取经纬度
            if result['status'] == 0:
                lat = result['result']['location']['lat']
                lng = result['result']['location']['lng']
                return lat, lng
            else:
                print('Error:', result.get('message', 'Unknown error'))
        else:
            print('Failed to get geocode:', response.status_code)

    def transform(self, address):
        s, e = self.get_address_encode(address)
        result = str(s) + "," + str(e)
        return result
    def is_lat_lng(self, text) -> bool:
        if "," in text:
            return True
        return False
    def path_planing(self, start_point:str, end_point:str) -> Dict:
        if not self.is_lat_lng(end_point):
            start_point = self.transform(start_point)
            end_point = self.transform(end_point)
        url = 'https://api.map.baidu.com/directionlite/v1/driving?'

        # 请求参数
        params = {
            'ak': ak,
            'output': 'json',
            'origin': start_point,
            'destination': end_point
        }

        # 发送HTTP GET请求
        response = requests.get(url, params=params)
        result = {}
        if response.status_code == 200:
            # 解析JSON格式的响应内容
            result = response.json()
            # print(result)
        return result

    def parse_path_planing_result(self, result) -> List[List[SData]]:
        # result = self.path_planing(start_point,end_point)
        # start_point = (result['result']['origin']['lat'], result['result']['origin']['lng'])
        # end_point = (result['result']['destination']['lat'], result['result']['destination']['lng'])
        middle_point = []
        # 解析数据
        if result["message"] == 'ok':
            for i in result['result']['routes']:
                route = []
                for j in i['steps']:
                    k = SData(path=j["path"],instruction=j["instruction"])
                    route.append(k)
                middle_point.append(route)
            # pass
        else:
            print('Error:', result.get('message', 'Unknown error'))
        return middle_point
    def parse(self, start_point, end_point):
        result = self.path_planing(start_point,end_point)
        print(result)
        start_point = (result['result']['origin']['lng'], result['result']['origin']['lat'])
        end_point = (result['result']['destination']['lng'], result['result']['destination']['lat'])
        parse_result = self.parse_path_planing_result(result)
        # print("parse \n\n\n\n\n\n")
        return start_point,end_point,parse_result
    def get_html(self,start,end):
        # start = "哈尔滨工业大学威海"
        # end = "山东大学威海"
        start, end, middle = self.parse(start, end)
        with open("config.toml","r") as f:
            config = toml.load(f)
        browser_ak = config["agent4train"]["browser_ak"]
        html = Html(browser_ak, start, middle)
        html_temp = html.html
        return html_temp

if __name__ == '__main__':
    st = "113.34996543415,22.843338917576;113.34983562901,22.843158483807;113.34981568662,22.842928424156"
    s = SData(st)
    print(s)
    # api = BaiduAPI(ak)
    # # text = ""
    # # with open("result.json", "r") as f:
    # #     text = json.load(f)
    # import streamlit as st
    # if "start_point" not in st.session_state and "end_point" not in st.session_state and "middle_point" not in st.session_state:
    #     st.session_state.start_point, st.session_state.end_point , st.session_state.middle_point=  api.parse("哈尔滨工业大学威海校区", "山东大学威海校区")
    # ls = []
    # parse = st.session_state.middle_point[0]
    # for i in parse:
    #     for j in i.path:
    #         ls.append(list(j))
    # # print(ls)
    #
    # folium_map = folium.Map(location=st.session_state.start_point, zoom_start=16)
    # for i in range(len(ls) - 1):
    #     # print(list(ls[i]))
    #     folium.Polygon(
    #             locations=[
    #                 list(ls[i]),
    #                 list(ls[i+1]),
    #
    #             ],
    #             popup=folium.Popup('标记坐标点之间多边形区域', max_width=200),
    #             color='blue',  # 线颜色
    #             fill=False,  # 是否填充
    #             weight=3,  # 边界线宽
    #         ).add_to(folium_map)
    # folium_map.add_child(folium.LatLngPopup())
    # output = st_folium(folium_map, width=700, height=500)
    # if output['last_clicked']:
    #     st.write('点击位置的经纬度为:')
    #     st.write(f"纬度: {output['last_clicked']['lat']}, 经度: {output['last_clicked']['lng']}")
