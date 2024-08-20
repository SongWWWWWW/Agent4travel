# Agent4train
> [!IMPORTANT]
> **重大更新：**
> 2024/8/14: 更新内容
> 1. 将agent，backend，frontend，Model，tools部分分开
> 2. 将所有配置全部集中在配置文件
> 3. 将agent流程分开，分为SuperAgent和ToolsAgent，重写对话流程
> 4. 将模型问答，baidu api 调用放置到后端api中 

> 2024/8/20: 更新内容
> 1. 添加tool, 多地点路线规划，景点图片查询，某地景点查询
> 2. 添加图片展示
> 3. 添加后端api


### 按照下面这个步骤进行环境配置
```bash
conda create -n agent4train python=3.12
conda activate agent4train
pip install -r requirements.txt
```
```bash
# 请将config.toml.temp更名为config.toml,并将环境变量填入
#启动👇
python backend/api.py # 启动后端
streamlit run main.py # 启动前端
```
### 效果展示
[示例视频](https://github.com/SongWWWWWW/Agent4train/blob/master/video.mp4)