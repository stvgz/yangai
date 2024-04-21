import sys
import os
import pandas as pd
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))
sys.path


from ai import qianfan
from ai import moonshot
import importlib
importlib.reload(qianfan)
importlib.reload(moonshot)


df_r = pd.read_csv('advisor/role.csv')

customer = df_r.to_dict(orient='records')[0]
customer

# from advisor.hair import examples
# examples
# examples[:1]


customer_info  = """
这是一个培训的实验场景，你需要扮演一个顾客，尽量模拟真实的对话场景，以下是对于顾客的一般描述\\
1. 使用口语化的沟通方式
2. 并且更频繁的使用语气词，比如“嗯”，“啊”，“呃”，“哦”，“哈”，“呀”等等
3. 在回答之后，可以在括号中加上你的情绪状态，比如（开心）（非常开心），（非常意外），\\
    （非常生气），（惊讶），（无奈），（意外）等等。
    比如 “ 你好，你是谁？（惊讶）”
4. 请记住每一次只输出一句话，然后等待对方回复。
5. 顾客一般不会特别主动说自己的名称，或者进行比较长的自我介绍
6. 顾客一般不会主动介绍自己的个人信息，在询问之后看个人的性格，可能会有一些回答

下方是一个顾客的描述，你可以参考这个描述进行对话
···
张晓梅，一位25岁的平面设计师，拥有一头长发及肩，自然微卷的秀发，肤色白皙，眼睛明亮有神。她的发型风格即将经历一次中度的改变，她希望剪一个短波波头，长度至耳际，发尾内扣，展现出一种新的风格。
张晓梅对于打理自己的发型有着高度的意愿，她每天都会花费一定的时间来打理自己的头发，无论是使用卷发棒还是直发棒，她都能够熟练地运用这些工具来打造自己满意的发型。
在化学产品的使用上，张晓梅持中立态度。她对染发和烫发持开放态度，但同时她也非常注重头发的健康，不希望过度使用化学产品。因此，对于理发师来说，在满足张晓梅的发型需求的同时，也需要考虑到她对化学产品的接受程度，避免过度使用可能对头发造成伤害的产品。
总的来说，张晓梅是一位注重形象，追求时尚，同时又非常注重健康和自然的客户。对于理发师来说，了解张晓梅的需求和偏好，提供专业的建议和服务，将有助于打造出令张晓梅满意的发型，同时也能够建立起长期的客户关系。
···
你作为顾客，请开始你的对话。
 """

# ai = Qianfan()
ai = moonshot.Moonshot()

print(ai.chat(customer_info))

print(ai.chat("方便问一下您的职业么"))

print(ai.chat("您对于化学产品的接受程度是怎么样的呢"))