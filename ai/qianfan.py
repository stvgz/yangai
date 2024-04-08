
import requests
import json
import os
from ai.ai import AIBase
from ai.logger import logger

class Qianfan(AIBase):

    def __init__(self,
                ak = None,
                sk = None
                ):
        
        from dotenv import load_dotenv
        load_dotenv()
        ak = os.getenv("APIKEY_QIANFAN")
        sk = os.getenv("SK_QIANFAN")
        self.ak = ak
        self.sk = sk
        self.token = None

        # conversation control
        self.conv = None
        self.conv_len_max = 20
        self.conv_str_max = 10000

        # chat roles
        self.role = 'user'
        self.response_role = 'assistant'


        pass


    def get_token(self):

        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.ak, "client_secret": self.sk}
        self.token = str(requests.post(url, params=params).json().get("access_token"))
        return 


    def add_conv(self, msg, role = 'user'):
        if not self.conv:
            self.conv = []

        # add msg to conv
        self.conv.append({
            "role": role,
            "content": msg
        })

        return

    def proxy(self, msg, role = None, reponse_role = None):
        """Define proxy chat with Qianfan AI"""

        if not self.token:
            self.get_token()

        # url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + self.token

    
        # url= "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-3.5-8k-1222?access_token=" + self.token

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + self.token

        payload = json.dumps({
                "messages": self.conv
                })

        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)

        # prase reponse
        res = json.loads(response.text)

        res_text = res['result']

        return res_text

    def system_prompt(self,  prompt = None, system_name = 'system',):
        """Define system prompt and add into conversation"""
        
        if not prompt:
            prompt = "Welcome to Qianfan AI"

        self.add_conv(prompt, role = system_name)

        return

    def set_system_prompt(self, prompt = None, system_name = 'system'):
        self.system_prompt(prompt, system_name)


    def chat(self, msg, role = None, reponse_role = None):
        """Define multi-turn chat with Qianfan AI"""

        if not role:
            role = self.role
        if not reponse_role:
            reponse_role = self.response_role
        
        self.add_conv(msg, role)
        
        logger.info("conversation {}".format(self.conv))

        res_text = self.proxy(msg, role, reponse_role)

        logger.info("response {}".format(res_text))
        
        self.add_conv(res_text, reponse_role)
        
        return res_text


if __name__ == "__main__":
    ai = Qianfan()

    ai.get_token()

    print(ai.chat("how are you "))