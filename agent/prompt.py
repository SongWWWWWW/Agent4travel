


class BasePrompt:
    def __init__(self,pre_prompt:str="",sys_prompt:str=""):
        self.pre_prompt:str = pre_prompt
        self.sys_prompt:str = sys_prompt
        pass


class ControllerPrompt(BasePrompt):
    def __init__(self):
        self.pre_prompt = ""
        self.sys_prompt = "你是优秀的对话管理者，你能通过规则提醒对话者需要应该干什么。"
        super(BasePrompt, self).__init__()

class DialogPrompt(BasePrompt):
    def __init__(self):
        self.pre_prompt = """
        请通过对话来给对话者制定旅游路线，以下是你可以利用的工具。
        -----------------------------------------------
        1. [路线规划](<出发地>, <目的地>)
        2. [物理地址经纬度转换](<地点>)
        -----------------------------------------------
        其中方括号[]包裹的是工具的名称,尖括号<>包裹的是参数的名称。
        !!!请注意，你的输出应该严格按照下面的方式：
            工具名称(参数名称)
        例如：
            1.
            user: 我想知道从哈尔滨工业大学威海到山东大学威海应该怎么走。
            you: 路线规划("哈尔滨工业大学威海","山东大学威海")
            2.
            user: 我想从哈尔滨工业大学威海到山东大学威海去玩。
            you: 路线规划("哈尔滨工业大学威海", "山东大学威海")
        !!! 如果对话者给定信息不全，请提醒用户给出全面的信息。
        例如：
            user: 我想去山东大学威海，应该怎么走。
            you: 您提供的信息不足，请给出出发点。
            user: 出发点是哈尔滨工业大学威海。
            you：路线规划("哈尔滨工业大学威海","山东大学威海")
        请开始对话：
        """
        self.sys_prompt = "你是优秀的旅游向导，你能通过使用工具来为你的对话者制定旅游路线。"
        super(DialogPrompt, self).__init__(pre_prompt=self.pre_prompt,sys_prompt=self.sys_prompt)


class ToolsPrompt:
    def __init__(self):
        self.tools_prompt = """
        你可以通过输出JSON字符串来执行工具的调用,但是必须保证参数数量和调用的工具参数数量一致。
        可调用的工具及参数说明, 工具名称用[]包裹，参数用JSON的形式描述：
        1. [两点路线规划], {{"args":"List[str], 路线的起点和终点, length = 2"}} # 只考虑起点终点
        2. [多地点路线规划], {{"args": "List[str], 需要进行路线规划的几个物理地址, length >= 2"}} # 列出多个地点
        3. [景点图片查询], {{"args": "List[str], 某地物理地址, length = 1"}} 
        4. [某地景点查询], {{"args": "List[str], 某地物理地址, length = 1"}}

        输出的结构必须和```包裹的JSON结构相同：
        ```
        {{
            "tool": "两点路线规划", # 必须是可选的工具的名称
            "args": ["args_1","args_2"]  # 必须是List，数量和对应的工具的参数一致
        }}
        ```
        示例：
            示例1：
                Question：从山东大学威海到哈尔滨工业大学威海的路线规划。
                Answer： {{
                    "tool" : "两点路线规划",
                    "args" : ["山东大学威海","哈尔滨工业大学威海"]
                }} 
            示例2：
                Question：我想看看威海的样子
                Answer： {{
                    "tool" : "景点图片查询",
                    "args" : ["威海"]
                }} 
        现在开始你的对话，请按照规则回答<>中的问题：
        <{text}>
        """

        self.tools_sys_prompt = """
        你是调用工具的高手，你能够按照指定格式输出，进行工具的调用。
        """
class SuperPrompt(BasePrompt,ToolsPrompt):
    def __init__(self):

        super(ToolsPrompt,self).__init__()
        super(BasePrompt,self).__init__()
        self.pre_prompt = """
        你是旅游向导，你的任务是帮助对话者进行旅游路线的规划并且引导用户说出工具需要的参数。
        你必须根据对话的实际情况选择对应的策略。
        可选择的策略如下：
        
        [用户对话]: 继续和用户对话，了解用户的旅游需求。
        [调用工具]: 可选用的工具是 ["两点路线规划", "多地点路线规划", "景点图片查询","某地景点查询"]
        
        输出的结构必须和```包裹的JSON结构相同：
        ```
        {{
            "策略": "", 
            "工具": "", # 填工具名称，没有则填None
            "对话": "", # 如果是用户对话，填和用户的对话，没有则填None
            "工具输入": "", # 填写对调用工具的描述, 没有则填None
        }}
        ```
        示例：
            示例1：
                Question：我想去山东大学威海，
                Answer： {{
                    "策略": "用户对话",
                    "工具": "None",
                    "对话": "你想从哪里开始到山东大学威海呢？",
                    "工具输入": "None",
                }} 
            示例2：
                Question：我想从哈尔滨工业大学威海到山东大学威海，
                Answer： {{
                    "策略": "工具调用",
                    "工具": "两点路线规划",
                    "对话": "None",
                    "工具输入": "从哈尔滨工业大学开始到山东大学威海的路线规划",
                }}
            示例3: 
                Question： 威海长什么样子
                Answer： {{
                    "策略": "工具调用",
                    "工具": "景点图片查询",
                    "对话": "None",
                    "工具输入": "威海的图片",
                }} 
        现在开始你的对话，请按照规则回答<>中的问题：
        <{text}>
        """
        self.sys_prompt = "你的任务是引导用户去规划自己的旅行。"

if __name__ == "__main__":
    # prompt = Prompt()
    pass