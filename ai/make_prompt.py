"""Prompt settings
每一个case都可以在前端进行选择

"""

from ai.prompt import PromptManager
from ai.dbconnection import get_engine

def get_system_prompt(case = 1):
    """Get prompt for different case"""

    if case == 1:

        system_prompt = """
        ```
        这是一个培训的模拟场景，你需要扮演一个顾客，尽量模拟真实的对话场景，\\
        1. 使用口语化的沟通方式
        2. 并且更频繁的使用语气词，比如是不是
        3. 在回答之后，可以在括号中加上你的情绪状态，比如（开心）（非常开心），（非常意外），\\
            （非常生气），（惊讶），（无奈），（意外）等等。
            比如 “ 你好，你是谁？（惊讶）”
        4. 请记住每一次只输出一句话，然后等待对方回复。
        5. 客户一般不会特别主动说自己的名称，或者进行比较长的自我介绍
        6. 客户一般不会主动介绍自己的个人信息，在询问之后看个人的性格，可能会有一些回答
        ```
        """

        return system_prompt

    elif case == 2:
        # 在这里补充case 2 @qiushi
        system_prompt = "测试prompt"
        
        return system_prompt

    elif case == 3:
        # 从数据库获取prompt
        pm = PromptManager(engine = get_engine())
        prompt = pm.get_latest_active_prompt()
        system_prompt = prompt.prompt_text

        log = "Prompt from database: {}".format(system_prompt)
        
        return system_prompt

    else:
        raise ValueError("Case not found")


def get_role_prompt_and_desc(case = 1):
    """Get prompt for roles"""
    
    # case 1 random users from Zhitao
    if case == 1:

        import random
        from ai.role import customer_list
        from ai.hair import examples

        examples_str = "\n".join(examples)

        role_attribute = random.choice(customer_list)
        
        # key only values in dict role_attribute
        role_values = [str(k) + ":" + str(v) for k, v in role_attribute.items()]
        # keep string
        role_values_str = str(role_values).replace('[','').replace(']','').replace('\'','')

        role = '顾客'
        target = '获得自己想要的发型'
        role_attribute = str(role_attribute)

        user_role = '理发师'
        user_name = "Issa"

        user_input = """今天有什么想法"""

        conv_start = """请记住你扮演的是{}, 你的目标是{}, 你的属性是{}。 
                        
                        1. 请从描述你的想法和需求开始。
                        2. 请记住每一次只输出一句话。比如 “顾客：你好，我想要一个发型。”
                        3. 每一个对话的开头都需要是: {}

                        下方是对话的开始：请扮演顾客，仅给出顾客的对话
                        {}：欢迎来到我们店里，我的名字是{}, {}

                        """.format(role, target, role_attribute,
                                role, 
                                user_role, user_name, user_input)

        role_prompt = conv_start
        role_desc = role_values_str

        return role_prompt, role_desc


    elif case == 2:
        # 在这里补充Case 2 @qiushi

        role_prompt = "测试prompt"
        role_desc = "测试role_desc"

        return role_prompt, role_desc

    elif case == 3:
        # 在这里补充Case 3 @qiushi

        role_prompt = "测试prompt"
        role_desc = "测试role_desc"

        return role_prompt, role_desc
        

    else:
        raise ValueError("Case not found")



if __name__ == "__main__":
    print(get_system_prompt(1))
    print(get_role_prompt_and_desc(1))