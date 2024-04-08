
import requests
import json
import os
from ai.ai import AIBase
from ai.qianfan import Qianfan


class Moonshot(Qianfan):

    def __init__(self,
                ak = None,
                sk = None
                ):

        super().__init__(ak, sk)

        self.sk = os.getenv("APIKEY_MOONSHOT")

    # def get_token(self):
    #     """
    #     使用 AK，SK 生成鉴权签名（Access Token）
    #     :return: access_token，或是None(如果错误)
    #     """
    #     url = "https://aip.baidubce.com/oauth/2.0/token"
    #     params = {"grant_type": "client_credentials", "client_id": self.ak, "client_secret": self.sk}
    #     self.token = str(requests.post(url, params=params).json().get("access_token"))
    #     return 

    def proxy(self, msg, role = None, reponse_role = None):

        from openai import OpenAI

        client = OpenAI(
            api_key= self.sk,
            base_url="https://api.moonshot.cn/v1",
        )

        completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        # model="moonshot-v1-32k",
        # messages=[ 
        #     {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一些涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        #     {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
        # ],
        messages = [{"role":"user", "content": msg}],
        temperature=0.1,
        # limit length of user reponse
        max_tokens = 150,
        )
        res = completion.choices[0].message 
        # print(completion.choices[0].message)
        return res.content





if __name__ == "__main__":
    ai = Moonshot()
    print(ai.chat("how are you "))
