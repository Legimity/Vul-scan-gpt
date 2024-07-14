import configparser
import json
import dashscope

from gpt.prompt import *
from dashscope.api_entities.dashscope_response import Message

from utils.logger import ColoredLogger

logger = ColoredLogger().get_logger()


class ResultAnalyzer:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("conf/conf.ini")
        self.api_key = config.get("dashScope", "DASHSCOPE_API_KEY")
        self.model_name = config.get("dashScope", "MODEL_NAME")
        self.client = dashscope.Generation()

    def analyze_nmap_result(self, nmap_result):
        prompt = gen_nmap_prompt(nmap_result)
        try:
            messages = [Message(role="system", content=prompt), Message(role="user", content=Prompt.user_prompt)]
            response = self.client.call(
                model=self.model_name,
                api_key=self.api_key,
                messages=messages)
            content = json.loads(response["output"]["text"].strip('```json').split('```', 1)[0].strip())
            # content = json.loads(response["output"]["text"].strip('```json').strip('```').strip())
            return content
        except Exception as e:
            logger.info("调用大模型异常:{}".format(e))
        return {}

    def analyze_struct2_result(self, struct2_result):
        prompt = gen_struct2_prompt(struct2_result)
        try:
            messages = [Message(role="system", content=prompt), Message(role="user", content=Prompt.user_prompt)]
            response = self.client.call(
                model=self.model_name,
                api_key=self.api_key,
                messages=messages)
            content = json.loads(response["output"]["text"].strip('```json').split('```', 1)[0].strip())
            # content = response["output"]["text"]
            # content = json.loads(response["output"]["text"].strip('```json').strip('```').strip())
            return content
        except Exception as e:
            logger.info("调用大模型异常:{}".format(e))
        return {}

    def analyze_tpscan_result(self, tpscan_result):
        prompt = gen_tpscan_prompt(tpscan_result)
        try:
            messages = [Message(role="system", content=prompt), Message(role="user", content=Prompt.user_prompt)]
            response = self.client.call(
                model=self.model_name,
                api_key=self.api_key,
                messages=messages)
            # content = json.loads(response["output"]["text"])
            content = json.loads(response["output"]["text"].strip('```json').split('```', 1)[0].strip())
            # content = json.loads(response["output"]["text"].strip('```json').strip('```').strip())
            return content
        except Exception as e:
            logger.info("调用大模型异常:{}".format(e))
        return {}

    def analyze_vulmap_result(self, vulmap_result):
        prompt = gen_vulmap_prompt(vulmap_result)
        try:
            messages = [Message(role="system", content=prompt), Message(role="user", content=Prompt.user_prompt)]
            response = self.client.call(
                model=self.model_name,
                api_key=self.api_key,
                messages=messages)
            content = json.loads(response["output"]["text"].strip('```json').split('```', 1)[0].strip())
            # content = json.loads(response["output"]["text"].strip('```json').strip('```').strip())
            return content
        except Exception as e:
            logger.info("调用大模型异常:{}".format(e))
        return {}

    def analyze_nikto_result(self, nikto_result):
        prompt = gen_nikto_prompt(nikto_result)
        try:
            messages = [Message(role="system", content=prompt), Message(role="user", content=Prompt.user_prompt)]
            response = self.client.call(
                model=self.model_name,
                api_key=self.api_key,
                messages=messages)
            content = json.loads(response["output"]["text"].strip('```json').split('```', 1)[0].strip())
            # content = json.loads(response["output"]["text"].strip('```json').strip('```').strip())
            return content
        except Exception as e:
            logger.info("调用大模型异常:{}".format(e))
        return {}

    # TODO: 只有2-3个工具的扫描结果时，也要能够进行分析，下面参数写死了5个
    def analyze_result(self, nmap_result, tpscan_result, struct2_result, vulmap_result, nikto_result):
        prompt = gen_all_prompt(nmap_result, tpscan_result, struct2_result, vulmap_result, nikto_result)
        try:
            messages = [Message(role="system", content=prompt), Message(role="user", content=Prompt.user_prompt)]
            response = self.client.call(
                model=self.model_name,
                api_key=self.api_key,
                messages=messages)
            #content = json.loads(response["output"]["text"].strip('```json').split('```', 1)[0].strip())
            # content = json.loads(response["output"]["text"].strip('```json').strip('```').strip())
            content = response["output"]["text"]
            #print(content)
            return content

        except Exception as e:
            logger.info("调用大模型异常:{}".format(e))
        return {}


if __name__ == '__main__':
    result_path = "result/"
    with open(result_path + "Nmap_9304d080404a11ef90ad047c16004811.json", 'r', encoding='utf-8') as file:
        nmap_result = file.read()
    with open(result_path + "Struct2Scan_c89ee5a43eaa11ef876e907841e33bc8.json", 'r', encoding='utf-8') as file:
        struct2_result = file.read()
    with open(result_path + "TPScan_bc1eb2f63ec411efa992047c16004811.json", 'r', encoding='utf-8') as file:
        tpscan_result = file.read()
    with open(result_path + "Vulmap_e70881e83f3411efaafe825b09f17296.json", 'r', encoding='utf-8') as file:
        vulmap_result = file.read()
    with open(result_path + "Nikto_5d3d6c1e3f6911ef8846047c16004811.json", 'r', encoding='utf-8') as file:
        nikto_result = file.read()

    # analyze_nmap = ResultAnalyzer().analyze_nmap_result(nmap_result)
    # with open(result_path + "nmap_result", 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(analyze_nmap, ensure_ascii=False, indent=4))

    # analyze_struct2 = ResultAnalyzer().analyze_struct2_result(struct2_result)
    # print(analyze_struct2)
    # with open(result_path + "struct2_result", 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(analyze_struct2, ensure_ascii=False, indent=4))

    # analyze_tpscan = ResultAnalyzer().analyze_tpscan_result(tpscan_result)
    # with open(result_path + "tpscan_result", 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(analyze_tpscan, ensure_ascii=False, indent=4))
    #
    # analyze_vulmap = ResultAnalyzer().analyze_vulmap_result(vulmap_result)
    # with open(result_path + "vulmap_result", 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(analyze_vulmap, ensure_ascii=False, indent=4))
    #
    # analyze_nikto = ResultAnalyzer().analyze_nikto_result(nikto_result)
    # with open(result_path + "nikto_result", 'w', encoding='utf-8') as file:
    #     file.write(json.dumps(analyze_nikto, ensure_ascii=False, indent=4))
    analyze_all = ResultAnalyzer().analyze_result(nmap_result, tpscan_result, struct2_result, vulmap_result,
                                                  nikto_result)
    with open(result_path + "report", 'w', encoding='utf-8') as file:
        file.write(analyze_all)
