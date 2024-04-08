import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


from ai.qianfan import Qianfan

ai = Qianfan()

# ai.system_prompt("今天天气怎么样")

ai.get_token()

print(ai.chat("how are you "))

print(ai.chat("今天天气怎么样"))

