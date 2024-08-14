from typing import List, Tuple

from sdata import SData
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
html_temp = r"""
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
	<style type="text/css">
	body, html,#allmap {{width: 100%;height: 100%;overflow: hidden;margin:0;font-family:"微软雅黑";}}
    </style>
    <script src="//mapopen.bj.bcebos.com/github/BMapGLLib/TrackAnimation/src/TrackAnimation.min.js"></script>
	<script type="text/javascript" src="//api.map.baidu.com/api?type=webgl&v=1.0&ak={ak}"></script>
    <title>视角动画</title>
</head>
<body>
	<div id="allmap"></div>
</body>
</html>
<script type="text/javascript">
    // GL版命名空间为BMapGL
    // 按住鼠标右键，修改倾斜角和角度
	var bmap = new BMapGL.Map("allmap");    // 创建Map实例
	bmap.centerAndZoom(new BMapGL.Point{start}, 17);  // 初始化地图,设置中心点坐标和地图级别
    bmap.enableScrollWheelZoom(true);     // 开启鼠标滚轮缩放
    var path = {path};
    var point = [];
    for (var i = 0; i < path.length; i++) {{
        point.push(new BMapGL.Point(path[i].lng, path[i].lat));
    }}
    var pl = new BMapGL.Polyline(point);
    setTimeout('start()', 3000);
    function start () {{
        trackAni = new BMapGLLib.TrackAnimation(bmap, pl, {{
            overallView: true,
            tilt: 30,
            duration: 20000,
            delay: 300
        }});
        trackAni.start();
    }}
</script>
"""


"""
start 格式 (lng,lat)
path 格式  
{
        'lng': 116.297611,
        'lat': 40.047363
    }, {
    	'lng': 116.302839,
    	'lat': 40.048219
    }, 
"""
class Html:
    def __init__(self,ak,start: Tuple,path:List[List[SData]]):
        self.html = html_temp.format(ak=ak,start=str(start),path=self.transform_parse(path))
    def transform_parse(self,parse:List[List[SData]]):
        # SData.path  : List[Tuple]
        parse = parse[0]
        point = []
        for i in parse:
            for j in i.path:
                point.append({ "lng":j[1],"lat":j[0]})
        return str(point)




