from baiduAPI import BaiduAPI,ak

tools_dict = {
    "路线规划": BaiduAPI(ak).get_html,
    "坐标转换": BaiduAPI(ak).transform
}