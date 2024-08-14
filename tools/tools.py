from baiduAPI import BaiduAPI
import toml
import os,sys
# print(sys.path)
sys.path.append(os.path.dirname(__file__))

with open('config.toml', 'r') as f:
    config = toml.load(f)
    ak = config["agent4travel"]["ak"]

tools_dict = {
    "路线规划": BaiduAPI(ak).get_html,
    "坐标转换": BaiduAPI(ak).transform
}

if __name__ == '__main__':
    print(tools_dict)