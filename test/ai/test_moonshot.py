import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


from ai.moonshot import Moonshot

ai =Moonshot()

ai.system_prompt('你是一个好人')

print(ai.chat("how are you "))

print(ai.chat("今天天气如何"))

assert len(ai.conv) ==4 