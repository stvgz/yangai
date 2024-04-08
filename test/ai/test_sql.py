import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from ai.qianfan import Qianfan

ai = Qianfan()

ai.get_token()

res = ai.chat("""
# Table name: order_prediction
# Content of this table: prediction of orders,
# Columns of this table including
# Column 1: index, 
# Column 2: date, 日期
# Column 3: value, 订单预测的数量
# Column 4: Source, 预测来源

我的问题是：我们需要订单数量以及日期
请写一个标准的SQL去获取到相关的数据，请仅输出可执行的SQL语句，不用解释。

参考输出的格式
```
select * from order_prediction
```
""")

matched = re.findall(r"```(.*?)```", res, re.DOTALL)

assert len(matched) == 1

query = matched[0]

print(query)