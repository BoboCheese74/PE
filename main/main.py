from LLM import ConnectLLM
import yaml
from Bio import Entrez
from Bio import Medline
import datetime
import time


class Main:
    def __init__(self):
        with open('config.yaml', 'r') as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)


    def generate_outline(self, language:str, title:str, LLM='openai', lordImg=False, image_path=None):
        """
        通过gpt生成提纲内容（promt）
        :param language: str 语言类型 只有中文和英文 除了中文以外的输入都默认为英文
        :param title: str 文章标题
        :param LLM: str 使用的大语言模型名称
        :param image_path:
        :param lordImg:
        """
        cfg = self.config[LLM]
        client = ConnectLLM(LLM, api_key=cfg['api_key'], model=cfg['model'])

        if language == "中文" or 'chinese':
            language_output = (
                "请用英文写作习惯与语言风格来构思内容，然后将构思的内容转换成中文写作习惯与语言风格并输出，注意：最终只需要用中文输出。"
            )
        else:
            language_output = "请用英文输出，并注意正确运用英文论文中的时态。"

        # 如果要上传图片则调用该方法(仅限于gpt-4o gpt-4o-vision gpt-4-turbo等等模型)
        if lordImg:
            res = client.OpenAISDK_WithImg(
                prompt=f"""你是资深医学背景的编辑，我准备写一类文章，这类文章的撰写都有一定的格式和框架，我框定的<格式框架>如下。请根据下述要求，结合文章标题与图表，参考下述案例撰写。
                        撰写要求：
                        ```
                        - 请根据我给你提供的“统计结果”（也就是下述图/表数据）对本文设计的研究方法进行介绍。
                        - 请学习下述案例的写作格式和风格，同时结合提供的图/表数据，采用相似的风格进行写作，不要分段写作。
                        - 不要分段。
                        ```
                
                        输出要求：
                        ```
                        - 请直接输出内容，不需要给出任何说明性文字
                        - 输出的内容中不要出现“综上所述、总的来说、总之”等表达总结性的连接词
                        - {language_output}
                        - 请用一个段落输出
                        ```
                
                        注意：
                        - 只需要学习案例的格式和风格，不能抄袭案例中的内容
                        """,
                input = f"""
                        文章标题：
                        ```
                        {title}
                        ```    
                        """,
                image_path = image_path
            )

        else:
            res = client.OpenAISDK(
                prompt = f"""你是资深医学背景的编辑，我准备写一类文章，这类文章的撰写都有一定的格式和框架，请根据我给出的标题或背景，按要求撰写。
                        ```
                
                        撰写要求：
                        ```
                        - 请总结下述案例的写作格式和风格，结合下述材料，采用同样的写作格式和风格写作以下内容。
                        - 不要分段。
                        ```
                
                        输出要求：
                        - 直接输出撰写的内容，不需要给出任何说明性文字
                        - 输出的内容中不要出现“综上所述、总的来说、总之”等表达总结性的连接词
                        - {language_output}
                        """,
                input = f"""文章标题：
                        ```
                        {title}
            
                        """
            )

        return res


    def get_keyword(self, content:str, LLM='deepseek'):
        """
        通过提纲提取关键词（用deepseek）
        :param content: str 提纲内容
        :param LLM: str 使用的大语言模型名称
        """
        cfg = self.config[LLM]

        client = ConnectLLM(LLM, api_key=cfg['api_key'], model=cfg['model'])
        res = client.OpenAISDK(
            prompt=f"""你是PubMed搜索专家，擅长通过一句话，定位出关键词或关键词短语，并通过关键词、关键词短语或它们之间的组合，去PubMed中检索文章。

                    现在有一段写医学文章的段落主旨，请找出关键词，将关键词进行有效组合，组合不超过3个词，当然组合不是必须要，输出这样的关键词或组合。
                    要求你的输出能够去 PubMed 中检索出相关文章，这些文章可以用来作为撰写这段内容的参考文章，请给出满足上述要求的关键词、关键词短语或者有效的组合。
    
                    注意：你给出的[]内的关键词或组合，是PubMed检索的一次输入，请确保你给出的关键词或组合能够检索出有助于撰写主旨的文章。   
                     要求：
                     1.关键词或关键词短语，用<>括起来，（如：[Keyword], [Keyword phrases]）
                     2.关键词、关键词短语的组合，用<>括起来，组合内部用逗号分隔（如：[Keyword, Keyword phrases], [Keyword1, Keyword2], [Keyword phrases1], [Keyword phrases2]）
                     3.根据段落内容，按照词或组合的重要性由高到低排序，最多输出5个词和组合
                     4.只输出关键词、关键词短语或组合，不要加任何其他字符或说明性文字
                     5.用'英文'输出，所有输出单词均用'小写'字母
                     6.找不到合理关键词、关键词短语或组合时，输出可以是空
                     7.以json格式输出，keys: keywords
                    """,
            input = f"""
                     段落主旨：
                     ```
                     {content}
                     ```
                     """
        )

        import json
        keywords_markdown = f"""
                            {res}
                            """
        keywords = json.loads(keywords_markdown.strip().strip('```json').strip('```').strip())

        for _ in keywords:  #由于AI生成出来的json数据key值并不一定是keywords故进行此处理
            keywords = keywords[_]

        return keywords


    def search_pubmed(self, keywords, max_per_keyword=5, max_total=30):
        """
        根据关键词去pubmed检索文献（近10年，影响因子>0.001，每个关键词最多5篇，一共不超过30篇）
        :param keywords: list 关键词列表
        :param max_per_keyword: int 每个关键词最多返回的文献数量
        :param max_total: int 总共返回的文献数量
        """
        Entrez.email = self.config['email']

        now = datetime.datetime.now()
        end_date = now.strftime("%Y/%m/%d")
        start_date = (now - datetime.timedelta(days=365 * 10)).strftime("%Y/%m/%d")
        date_query = f'("{start_date}"[PDAT] : "{end_date}"[PDAT])'

        pmids = set()

        # 获取符合要求的PMID
        for keyword in (
                keywords.replace("'", "").replace('"', "").replace("[", "").replace("]", "").replace("\n", "").split(",")
        ):
            if len(pmids) >= max_total:
                break

            query = f'({keyword}) AND {date_query}'
            try:
                handle = Entrez.esearch(db="pubmed", term=query, retmax=max_per_keyword)
                time.sleep(0.334)  # 没有API密钥限制每秒请求3次
                record = Entrez.read(handle)
                handle.close()
            except Exception as e:
                print(f"搜索关键词'{keyword}'时出错: {e}")
                continue

            available_pmids = record.get('IdList', [])
            remaining = max_total - len(pmids)
            add_ids = available_pmids[:min(max_per_keyword, remaining)]
            pmids.update(add_ids)

        # 获取摘要内容
        abstracts = []
        num = 1
        for pmid in list(pmids)[:max_total]:
            try:
                handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
                time.sleep(0.334)
                records = list(Medline.parse(handle))
                handle.close()

                if records:
                    abstract = records[0].get('AB', '')
                    if abstract:
                        abstracts.append(f'文献[{num}]:' + abstract.strip())
                        num += 1
            except Exception as e:
                print(f"获取PMID {pmid}摘要失败: {e}")
                print('尝试跳过')

        return abstracts


    def edit(self, language:str, title:str, prompt_outline:str, paper, LLM='anthropic'):
        """
        Claude生成文章
        :param language: str 语言类型 只有中文和英文 除了中文以外的输入都默认为英文
        :param title: str 文章标题
        :param prompt_outline: str 提纲内容
        :param paper: str 文献内容
        :param LLM: str 使用的大语言模型名称
        """
        cfg = self.config[LLM]

        if language == "中文" or 'chinese':
            language_output = (
                "请用英文写作习惯与语言风格来构思内容，然后将构思的内容转换成中文写作习惯与语言风格并输出，注意：最终只需要用中文输出。"
            )
        else:
            language_output = "请用英文输出，并注意正确运用英文论文中的时态。"

        client = ConnectLLM(LLM, api_key=cfg['api_key'], model=cfg['model'])
        res = client.OpenAISDK(
            prompt = f"""你是资深医学编辑，请根据以下<写作思路>以及下述<参考文章>，按要求撰写医学论文。
                        具体要求如下:             
                        1. 写作要求:             
                        ```
                        <step1>首先，仔细阅读<写作思路>。理解写作思路的主题、子主题以及每句话的要点。
                        <step2>接下来，仔细阅读<参考文章>，对每篇文章的主要内容和观点有清晰的理解。
                        <step3>阅读<写作思路>进行撰写：
                        <step3.1>在写作过程中，每处最多应用3篇文章，请务必使用参考文章的编号作为引用标号。
                        <step3.2>你只能引用给定的<参考文章>来撰写，严禁创新或使用未提供的参考文章。
                        <step4>对于每个引用的内容，要在引用部分后添加参考文章编号[num]，注意编号的使用容易出错，此处要避免编号错误。
                        <step5>在写作过程中，如果发现找到的引用内容与写作思路有偏差，应以引用内容为准。不要试图改变引用内容去适应写作思路。
                        <step6>对于引用的数据内容，要确保与原文保持一致。避免因为理解错误或记忆错误导致与原文出现偏差。
                        <step7>在写作过程中，如果遇到写作思路中需要的内容在参考文章中找不到的情况，不要试图引用未提供的参考文章。
                        <step7.1>在这种情况下，要仔细阅读当前写作位置的上下文以及当前位置写作思路的上下文，根据参考文章知识，改变当前写作思路，用参考文章的知识进行撰写，切记不要引用未提供的参考文章。
                        <step8>在写作过程中，定期回顾和检查你的工作。确保每个引用的内容都与原文一致。
                        <step9>对于每个引用的信息，都要对照原文进行校对。避免因为记忆错误或理解错误导致写作错误。
                        注意：a) 我只提供了参考文章的编号，标题和摘要，请用这些内容进行参考。
                        b) 每个位置引用文献数量最多3篇。
                        ```
    
                        2. 预期输出要求:
                        ```
                        - 参考原文内容时请务必准确无误，一字不差地引用原文的数字和表述。
                        - 请直接参考原文，避免转述可能带来的误差。
                        - 所参考的内容必须来自于我提供的参考文章,尤其是涉及到数字的部分,务必保持准确无误。
                        - 请确保所撰写的内容都有据可依，保持科学严谨,不要编造不存在的结论或数据。
                        - 撰写内容中引用标识格式：
                        -- 如果没有特别说明，参考文章引用标号需要放在每个引用句子的句尾。
                        -- 引用标号的正确格式：[num]，或[num1,num2]。
                        - 只需输出段落内容，结尾处不需要给出参考文章信息。
                        ```
                        """,
            input = f"""文章标题：```{title}```
    
                        写作思路：
                        ```
                        {prompt_outline}
                        ```
                        
                        3. 参考文章:
                        ```
                        {paper}
                        ```            
    
                        注意！！每个位置最多只能引用3篇文章。
    
                        请根据上述材料撰写内容,并注意以下事项:
                        a) 不要出现“综上所述、总的来说、总之”等表达总结性的词
                        b) 请直接输出内容，不要添加任何说明性文字
                        c) 不要分段
                        d) {language_output}
                        """
            )

        return res


if __name__ == '__main__':
    Main = Main()

    outline = Main.generate_outline("中文", "基于SHR（应激性高血糖比值）构建STEMI患者短期不良预后的预测模型", LLM='deepseek')
    print("提纲:", outline)

    keywords = Main.get_keyword(outline)
    print("提纲的关键词:", keywords)

    articles = Main.search_pubmed(keywords)
    print("文献:", articles)
    article = Main.edit(
        "中文",
        "基于SHR（应激性高血糖比值）构建STEMI患者短期不良预后的预测模型",
        outline,
        articles,
        LLM='deepseek'
    )
    print("文章:", article)
