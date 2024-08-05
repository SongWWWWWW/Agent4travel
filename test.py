# import requests
# from baiduAPI import  BaiduAPI
# # 您的百度地图API密钥
ak = 'DtHkmsbgV76BWBIrlYYM6wsoUV9BM6UX'
#
# def transform(ak,address):
#     s, e = BaiduAPI(ak).get_address_encode(address)
#     result = str(s) + "," + str(e)
#     return result
#
# # 起点和终点，格式为"经度,纬度"
# start_point = '大连信华信员工宿舍'# 例如：天安门广场
# start_point = transform(ak,start_point)
# end_point = '星海广场'    # 例如：北京首都国际机场
# end_point = transform(ak,end_point)
# # 路径规划API的URL
# url = 'https://api.map.baidu.com/directionlite/v1/driving?'
#
# # 请求参数
# params = {
#     'ak': ak,
#     'output': 'json',
#     'origin': start_point,
#     'destination': end_point
# }
#
# # 发送HTTP GET请求
# response = requests.get(url, params=params)
#
# if response.status_code == 200:
#     # 解析JSON格式的响应内容
#     result = response.json()
#     print(result)
#     # 检查API状态码
#     if result.get('status') == 0 and result.get('result'):
#         # 提取路径规划结果
#         routes = result['result']['routes']
#         for route in routes:
#             # 打印路线的起点和终点坐标
#             print(f"起点坐标: {route['start_point']['location']}")
#             print(f"终点坐标: {route['end_point']['location']}")
#
#             # 打印路线的总距离和预计行驶时间
#             print(f"总距离: {route['distance']}米")
#             print(f"预计行驶时间: {route['duration']}分钟")
#
#             # 提取并打印路线的分段信息
#             for step in route.get('steps', []):
#                 print(f"- 路段: {step['instruction']}")
#                 if 'path' in step:
#                     path_coords = step['path']
#                     print(f"  坐标点数: {len(path_coords)}")
#         print("\n")
#     else:
#         print('API调用失败:', result.get('message', '未知错误'))
# else:
#     print('请求失败:', response.status_code)

# import streamlit as st
# import pydeck
# st.markdown('''
#     <style>
#     body {
#         font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
#     }
#     .st-eg {
#         font-size: 16px !important;
#     }
#     .st-rg {
#         font-size: 16px !important;
#     }
#     .st-cs {
#         font-size: 16px !important;
#     }
#     .st-bf {
#         font-size: 16px !important;
#     }
#     .st-fm {
#         font-size: 16px !important;
#     }
#     .st-df {
#         font-size: 16px !important;
#     }
#     .st-de {
#         font-size: 16px !important;
#     }
#     .st-tb {
#         font-size: 16px !important;
#     }
#     .st-fg {
#         font-size: 16px !important;
#     }
#     .st-txs {
#         font-size: 16px !important;
#     }
#     .st-hc {
#         font-size: 16px !important;
#     }
#     .st-wn {
#         font-size: 16px !important;
#     }
#     .st-el {
#         font-size: 16px !important;
#     }
#     .st-is {
#         font-size: 16px !important;
#     }
#     .st-rs {
#         font-size: 16px !important;
#     }
#     .st-rm {
#         font-size: 16px !important;
#     }
#     .st-ml {
#         font-size: 16px !important;
#     }
#     .st-mi {
#         font-size: 16px !important;
#     }
#     .st-di {
#         font-size: 16px !important;
#     }
#     .st-sg {
#         font-size: 16px !important;
#     }
#     .st-ld {
#         font-size: 16px !important;
#     }
#     .st-vc {
#         font-size: 16px !important;
#     }
#     .st-tb .st-eg {
#         font-size: 16px !important;
#     }
#     .st-fg .st-eg {
#         font-size: 16px !important;
#     }
#     .st-txs .st-eg {
#         font-size: 16px !important;
#     }
#     </style>
# ''')
# # 定义点数据，每个点包含经度、纬度和大小
# points_data = [
#     {"lng": 116.397428, "lat": 39.90933, "size": 30},
#     {"lng": 121.487899, "lat": 31.249162, "size": 20}
# ]
#
# # 定义边数据，边由起点和终点的索引组成
# edges_data = [
#     {"source": 0, "target": 1}
# ]
#
# # 创建点图层
# scatter_layer = pydeck.Layer(
#     'ScatterLayer',
#     data=points_data,
#     get_position=['lng', 'lat'],
#     get_size='size',
#     pickable=True,
# )
#
# # 创建边图层
# line_layer = pydeck.Layer(
#     'LineLayer',
#     data=edges_data,
#     sources=[0],
#     targets=[1],
#     get_source_position='lng',
#     get_target_position='lat',
# )
#
# # 创建地图视图，并添加图层
# deck = pydeck.Deck(
#     initial_view_state={
#         'latitude': 39.90933,  # 中心点纬度
#         'longitude': 116.397428,  # 中心点经度
#         'zoom': 5.5,  # 缩放级别
#     },
#     layers=[scatter_layer, line_layer],
# )
#
# # 在 Streamlit 中显示地图
# st.pydeck_chart(deck)


# import streamlit as st
# import folium
# from streamlit_folium import st_folium
#
#
# # 创建 Streamlit 应用
# def main():
#     st.title('Click on the map to get coordinates')
#
#     # 创建 Folium 地图
#     folium_map = folium.Map(location=[39.998586, 116.328908], zoom_start=16)
#
#     # 加边
#     folium.Polygon(
#         locations=[
#             [39.998586, 116.328908],
#             [40.001528, 116.32408],
#
#         ],
#         popup=folium.Popup('标记坐标点之间多边形区域', max_width=200),
#         color='blue',  # 线颜色
#         fill=False,  # 是否填充
#         weight=3,  # 边界线宽
#     ).add_to(folium_map)
#     folium.Polygon(
#         locations=[
#
#             [40.001528, 116.32408],
#             [40.005251, 116.322299],
#         ],
#         popup=folium.Popup('标记坐标点之间多边形区域', max_width=200),
#         color='blue',  # 线颜色
#         fill=False,  # 是否填充
#         weight=3,  # 边界线宽
#     ).add_to(folium_map)
#     # 添加点击事件
#     folium_map.add_child(folium.LatLngPopup())
#
#     # 在 Streamlit 中显示 Folium 地图
#     output = st_folium(folium_map, width=700, height=500)
#
#     # 如果有点击事件，显示经纬度
#     if output['last_clicked']:
#         st.write('点击位置的经纬度为:')
#         st.write(f"纬度: {output['last_clicked']['lat']}, 经度: {output['last_clicked']['lng']}")
#
#
# if __name__ == '__main__':
#     main()
# text = ""
# with open("test.txt", "r", encoding="utf-8") as f:
#     for index, line in enumerate(f.readlines()):
#         print(line)
#         print(index)
#         text = line
# text = eval(text)
# print(type(text))
# with open("test.json", "w", encoding="utf-8") as f:
#     json.dump(text, f, ensure_ascii=False)
# print(type(text["result"])) # dict
# for k ,v in text["result"].items():
#     print(k)
#     # origin
#     # destination
#     # routes
# print(type(text["result"]["origin"]))
# # for k,v in text["result"]["origin"]:
# #     print(k)
# print(text["result"]["origin"])
# print(type(text["result"]["destination"]))
# print(text["result"]["destination"])
# # for k in text["result"]["origin"]:
# #     print(k)
# print(type(text["result"]["routes"]))
# print(text["result"]["routes"][0])
# print(json.dumps(text, indent=4, sort_keys=True))

# from baiduAPI import BaiduAPI, ak
# ak = ak
# baiduapi = BaiduAPI(ak)
# result = baiduapi.path_planing("清华大学","北京大学")
# print(result)
# text = {}
# with open("result.json","r",encoding="utf-8") as f:
#     text = json.load(f)
# print(len(text["result"]["routes"][0]["steps"]))
# # print(len(text["result"][""]))
# text = json.dumps(text,indent=4,sort_keys=True)
# print(text)

# 设置页面标题和布局
# st.set_page_config(page_title="地图单击拾取经纬度", layout="wide")

# 定义HTML模板
# html_temp = """
# <!DOCTYPE html>
# <html lang="zh-CN">
# <head>
#     <meta charset="utf-8">
#     <title>添加图文组合信息窗口</title>
#     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
#     <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
#     <meta http-equiv="X-UA-Compatible" content="IE=Edge">
#     <style>
#     body,
#     html,
#     #container {
#         overflow: hidden;
#         width: 100%;
#         height: 100%;
#         margin: 0;
#         font-family: "微软雅黑";
#     }
#     </style>
#     <script src="//api.map.baidu.com/api?type=webgl&v=1.0&ak=HI4GMK7McQZzaGdsoiD8gPA2exGdSbJf"></script>
# </head>
# <body>
#     <div id="container"></div>
# </body>
# </html>
# <script>
# var map = new BMapGL.Map('container');
# map.centerAndZoom(new BMapGL.Point(116.404, 39.915), 15);
# map.enableScrollWheelZoom(true);
# // 创建添加点标记
# var marker = new BMapGL.Marker(new BMapGL.Point(116.404, 39.915));
# map.addOverlay(marker);
# // 创建图文信息窗口
# var sContent = `<h4 style='margin:0 0 5px 0;'>天安门</h4>
#     <img style='float:right;margin:0 4px 22px' id='imgDemo' src='https://www.bijingdi.com/uploadfile/2021/1125/20211125095434694.jpg' width='139' height='104'/>
#     <p style='margin:0;line-height:1.5;font-size:13px;text-indent:2em'>
#     天安门坐落在中国北京市中心,故宫的南侧,与天安门广场隔长安街相望,是清朝皇城的大门...
#     </p></div>`;
# var infoWindow = new BMapGL.InfoWindow(sContent);
# // marker添加点击事件
# marker.addEventListener('click', function () {
#     this.openInfoWindow(infoWindow);
#     // 图片加载完毕重绘infoWindow
#     document.getElementById('imgDemo').onload = function () {
#         infoWindow.redraw(); // 防止在网速较慢时生成的信息框高度比图片总高度小，导致图片部分被隐藏
#     };
# });
# </script>
# """
# html_temp = r"""
# <!DOCTYPE html>
# <html>
# <head>
# 	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
# 	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
# 	<style type="text/css">
# 	body, html,#allmap {{width: 100%;height: 100%;overflow: hidden;margin:0;font-family:"微软雅黑";}}
#     </style>
#     <script src="//mapopen.bj.bcebos.com/github/BMapGLLib/TrackAnimation/src/TrackAnimation.min.js"></script>
# 	<script type="text/javascript" src="//api.map.baidu.com/api?type=webgl&v=1.0&ak=f{ak}"></script>
#     <title>视角动画</title>
# </head>
# <body>
# 	<div id="allmap"></div>
# </body>
# </html>
# <script type="text/javascript">
#     // GL版命名空间为BMapGL
#     // 按住鼠标右键，修改倾斜角和角度
# 	var bmap = new BMapGL.Map("allmap");    // 创建Map实例
# 	bmap.centerAndZoom(new BMapGL.Point{start}, 17);  // 初始化地图,设置中心点坐标和地图级别
#     bmap.enableScrollWheelZoom(true);     // 开启鼠标滚轮缩放
#     var path = [{path}];
#     var point = [];
#     for (var i = 0; i < path.length; i++) {{
#         point.push(new BMapGL.Point(path[i].lng, path[i].lat));
#     }}
#     var pl = new BMapGL.Polyline(point);
#     setTimeout('start()', 3000);
#     function start () {{
#         trackAni = new BMapGLLib.TrackAnimation(bmap, pl, {{
#             overallView: true,
#             tilt: 30,
#             duration: 20000,
#             delay: 300
#         }});
#         trackAni.start();
#     }}
# </script>
# """
# start = "哈尔滨工业大学威海"
# end = "山东大学威海"
# start ,end , middle = BaiduAPI(ak).parse(start,end)
# ak = "HI4GMK7McQZzaGdsoiD8gPA2exGdSbJf"
# html = Html(ak,start,middle)
# html_temp = html.html
# print(html_temp)
# st.write("hello")
# # 渲染HTML组件
# html_component = st.components.v1.html(html_temp, height=600)
#
# # 显示经纬度
# if html_component:
#     st.write(f"点击位置经纬度: {html_component}")
# s = []
# s.append({"hello":1,"hhe":12})
# print(s)


import streamlit as st
import time
full_string="hello world"
display_string=""
show_string=st.empty()
st.markdown("other content")
for c in full_string:
	display_string+=c
	show_string.markdown(display_string)
	time.sleep(1)