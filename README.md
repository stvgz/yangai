# Yangai

An AI assistant for all 


ref blackboxdata.cloud


# Quick Start

应用启动
> python manager.py

> http://127.0.0.1:8050/ai/


场景1：
用户列表
内置的用户列表
prompt

app/chat_basic.py


场景2：
1. system prompt 代码补充
2. role prompt 代码补充

场景3：

1. system prompt用数据库最新一条
2. role prompt 自己补充



# Repo

advisor: 理发师的定义，和一些角色的定义，role.csv,如果是case1，会在所有的role进行随机选择
ai: ai component
    model: DB的一些交互的对象
    
    ai: AIBase class
    qianfan: derived from AIBase
    moonshot: derived from Qianfan


        ai = Qianfan()
        res = ai.chat("今天你好么？")
        ai.conv = [
                {},
                {},
                {}
                ]

app: frontend application with Dash
    chat_basic.py: core application
    chat_components: some components
    urls.py: multi-application management
    

.env
manager.py: main file to run application


# How to

New scenario, goto  make_prompt.py ->  get_role_prompt_and_desc

ai.chat(system_prompt + role_prompt)



## Change Model