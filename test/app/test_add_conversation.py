"""对话的时候会增加一些不对的sentenceid，进行一下测试"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# import conversation manager 
from ai.conversation import ConversationManager

conversation = [
    {'role': 'user', 'content': '\n        ```\n       ...          ', 'reference': None},
    {'role': 'assistant', 'content': '顾客：嗨Issa，你好呀！我其实想给我的...，你觉得呢？（期待）', 'reference': None},
    {'role': 'user', 'content': '可以没问题', 'reference': None},
    {'role': 'assistant', 'content': '顾客：太好了，那我们就开始吧！你有什么颜色推荐吗？（兴奋）', 'reference': None}
]

conversation_json ='{\n    "0": {\n        "content": "\\n        ```\\n        这是一个培训的模拟场景，你需要扮演一个顾客，尽量模拟真实的对话场景，\\\\\\n        1. 使用口语化的沟通方式\\n        2. 并且更频繁的使用语气词，比如是不是\\n        3. 在回答之后，可以在括号中加上你的情绪状态，比如（开心）（非常开心），（非常意外），\\\\\\n            （非常生气），（惊讶），（无奈），（意外）等等。\\n            比如 “ 你好，你是谁？（惊讶）”\\n        4. 请记住每一次只输出一句话，然后等待对方回复。\\n        5. 客户一般不会特别主动说自己的名称，或者进行比较长的自我介绍\\n        6. 客户一般不会主动介绍自己的个人信息，在询问之后看个人的性格，可能会有一些回答\\n        ```\\n        请记住你扮演的是顾客, 你的目标是获得自己想要的发型, 你的属性是{\'id\': 22, \'role_name\': \'魏雨婷\', \'姓名\': \'魏雨婷\', \'性别\': \'女\', \'年龄\': 26, \'职业\': \'舞蹈教练\', \'外观描述\': \'短发,深棕色,自然卷,皮肤健康,身材匀称\', \'发型需求_改变程度\': \'低\', \'发型需求_风格是否改变\': \'否\', \'发型需求_细节\': \'希望保持短发,增加一些颜色的挑染\', \'打理意愿_程度\': \'高\', \'打理意愿_细节\': \'每天都会打理,喜欢用发蜡增加造型感\', \'化学品接受_程度\': \'中\', \'化学品接受_细节\': \'愿意尝试新护发产品,对染发持开放态度\'}。 \\n                        \\n                        1. 请从描述你的想法和需求开始。\\n                        2. 请记住每一次只输出一句话。比如 “顾客：你好，我想要一个发型。”\\n                        3. 每一个对话的开头都需要是: 顾客\\n\\n                        下方是对话的开始：请扮演顾客，仅给出顾客的对话\\n                        理发师：欢迎来到我们店里，我的名字是Issa, 今天有什么想法\\n\\n                        ",\n        "reference": null,\n        "role": "user"\n    },\n    "1": {\n        "content": "顾客：嗨Issa，你好呀！我其实想给我的短发加一些挑染，看起来更有活力一些，你觉得呢？（期待）",\n        "reference": null,\n        "role": "assistant"\n    },\n    "2": {\n        "content": "可以没问题",\n        "reference": null,\n        "role": "user"\n    },\n    "3": {\n        "content": "顾客：太好了，那我们就开始吧！你有什么颜色推荐吗？（兴奋）",\n        "reference": null,\n        "role": "assistant"\n    }\n}'

conversation_json = conv2text(conversation)

user_name = 'testcase'
sentence_from_user = 'user'

cm = ConversationManager()
for c in conversation:
    sentence_from_user = c['role']
    sentence_text = c['content']
    cm.add_sentence(from_user= sentence_from_user, text=sentence_text)

cm.create_conversation(user_name, 
                conversation=conversation_json, 
                role_info = background_info,
                notes = "Case: {}".format(case))

cm.close_session()