import base64
from openai import OpenAI


class ConnectLLM:
    def __init__(self, LLM:str, api_key: str, model: str):
        """
        LLM: str 使用的LLM名称 如openai deepseek anthropic(即Claude) 理论上支持所有兼容OpenAI SDK的LLM
        api_key: str API密钥
        model: str 模型名称 ChatGPT默认gpt-3.5-turbo DeepSeek默认deepseek-chat(即deepseek_V3)
        """
        self.LLM = LLM
        self.api_key = api_key
        self.model = model


    def OpenAISDK(self, prompt:str, input:str, temperature=1.5, max_tokens=4096, stream:bool=False):
        """
        temperature: float 推荐参数: 代码生成/数学解题0.0 数据抽取/分析1.0 通用对话1.3 翻译1.3 创意类写作/诗歌创作1.5
        max_tokens: int 最大token数
        prompt: str 提示语
        input: str 输入内容
        stream: bool 是否使用流式输出
        """
        client = OpenAI(api_key=self.api_key, base_url=f'https://api.{self.LLM}.com/v1')

        response = client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input},
            ],
            stream=stream
        )

        return  response.choices[0].message.content


    def OpenAISDK_WithImg(self, prompt:str, input:str, image_path):
        """
        本地图片上传
        通过OpenAI的API进行图像处理 仅支持gpt-4o gpt-4o-vision gpt-4-turbo等等模型 更多的请参考 https://platform.openai.com/docs/models
        :param prompt:
        :param input:
        :param image_path:
        :return:
        """
        if image_path is None:
            raise ValueError("image_path cannot be None")
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        client = OpenAI(api_key=self.api_key, base_url=f'https://api.{self.LLM}.com/v1')

        response = client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": input},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    ],
                }
            ],
        )
        return response.output_text


if __name__ == '__main__':
    deepseek = ConnectLLM(LLM='deepseek',api_key='',model='deepseek-chat')
    print(deepseek.OpenAISDK(
                             prompt='你是一个医学编辑助手',
                             input='请帮我写一段关于心脏病的介绍')
          )
