from abc import abstractmethod

class AIBase():

    def __init__(self):

        self.ak = ak
        self.sk = sk
        self.token = None

        # conversation control

        # conversation 
        # conv = [
                    # {'role': 'user', 'content': '你好'},
                    # {'role': 'system', 'content': '你好，我是 Moonshot AI，有什么可以帮助你的？'}
        #       ]
        self.conv = None
        self.conv_len_max = 20
        self.conv_str_max = 10000

        return
    
    @abstractmethod
    def get_token():
        pass

    @abstractmethod
    def chat():
        pass





