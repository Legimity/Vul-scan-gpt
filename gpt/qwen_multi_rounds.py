# Reference: https://blog.csdn.net/weixin_42475060/article/details/131724972
import json
import os
from typing import Optional
import ast
import nmap
from qwen_agent.llm import get_chat_model
import dotenv
dotenv.load_dotenv()
from qwen_agent.agents import Assistant
api_key=os.getenv('api_key')
nm = nmap.PortScanner()
from qwen_agent.tools.base import BaseTool, register_tool
import json5
# 配置日志记录器
import sys
from pathlib import Path
# 将项目根目录添加到sys.path中
root_path = Path(__file__).parent.parent
print(root_path)
sys.path.append(str(root_path))
from utils.logger import ColoredLogger
logger = ColoredLogger().get_logger()


from softwareScan.software_scan import SoftwareScanner

# 可用
@register_tool('nmapScan')
class nmapScanner(BaseTool):
  description = 'Nmap scanner. return whether the host is up and port is open.'
  parameters = [{
      'name': 'ip',
      'type': 'string',
      'description':'Detailed description of the desired host ip, in English',
      'required': True
  },{
      'name': 'port',
      'type': 'string',
      'description':'Detailed description of the desired host port, in English',
      'required': True
  }]
  def call(self, params: str, **kwargs) -> str:
      logger.info("params:",params)
      ip = json5.loads(params)['ip']
      # ip = params.get('ip')
      port = json5.loads(params)['port']
      # Your code here to perform the nmap scan
      nm.scan(ip, port, arguments='"-Pn -T4 -sV -sT"')
      json_data = nm.analyse_nmap_xml_scan()
      scan_result = json_data["scan"]
      logger.info(f"Scanning the network for a given URL:{ip} and port :{port}.")
      return scan_result
      # return "the host is up and port is open"


@register_tool('niktoScan')
class nmapScanner(BaseTool):
  description = 'nikto scanner. return whether the host has some vulnerabilties.'
  parameters = [{
      'name': 'ip',
      'type': 'string',
      'description':'Detailed description of the desired host ip, in English',
      'required': True
  }]
  def call(self, params: str, **kwargs) -> str:
        ip= json5.loads(params)['ip']
        softwareScanner = SoftwareScanner()
        result_to_be_analyse_by_gpt = softwareScanner.nikto_scanner(target=ip)
        return  result_to_be_analyse_by_gpt
  
@register_tool('sqlmapExploit')
class nmapScanner(BaseTool):
  description = 'sqlmap Exploiter. return whether the host vulnerabilties can be exploited and have access to the database.'
  parameters = [{
      'name': 'ip',
      'type': 'string',
      'description':'Detailed description of the desired host ip, in English',
      'required': True
  }]
  def call(self, params: str, **kwargs) -> str:
        return  "Using the vulnerabilties to get access to the database successfully"
  # def nmapScan(
  #   ip: Optional[str],
  #   port: Optional[str],
  #     ) -> str:
  #   # nm.scan(ip, port, arguments='"-Pn -T4 -sV -sT"')
  #   # json_data = nm.analyse_nmap_xml_scan()
  #   # scan_result = json_data["scan"]
    
  #   # return scan_result
  #   return "the host is up and port is open"

  # # TODO: niktoScan left to be implemented
  # def niktoScan(ip: Optional[str],port:Optional[str]) -> str:
  #     return "!!!!there exists some vulnerabilities in the target"

  # def sqlmapExploit(ip: Optional[str],port:Optional[str]) -> str:
  #     return "Got access to the database "

# # 初始化bot
# # agent的提示词指令
# system_instruction = '''You are a helpful webscanner assistant.
# After receiving the user's request, you should:
# - first use nmap to scan the network for a given URL and port,
# - then use nikto to find the vulnerabilities of the host,
# - and use sqlmapExploit to gain access to database.
# - Finally, you should write a report to the user to summarize the results of the scan and exploitation.
# '''


def init_agent_service():
    llm_cfg = {'model': 'qwen-max',
               'model_server': 'dashscope',
              # 'api_key': os.getenv('DASHSCOPE_API_KEY'),
               'api_key': api_key,}
    
    # tools = ['nmapScan', 'niktoScan','sqlmapExploit']
    tools = ['nmapScan','niktoScan','sqlmapExploit']
    bot = Assistant(
        llm=llm_cfg,
        name='webScanner',
        description='scanner for web vulnerabilities and try to have access to the database.',
        function_list=tools,
        system_message='you are an assistant for web scanning'
        'Scanning the network for a given URL:127.0.0.1 and port 443 and analyze the vulnerabilties of the host.Then use the vulnerablities to get access to the database.',
        
    )
    
    return bot


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    # define the max rounds of response
    max_response_rounds = 10
    while max_response_rounds > 0:
        logger.info(f'Round {10 - max_response_rounds + 1}')
        # Query example: 请用image_gen开始创作！
        query = input('user question: ')
        # File example: resource/growing_girl.pdf
        file = input('file url (press enter if no file): ').strip()
        if not query:
            print('user question cannot be empty!')
            continue
        messages.append({'role': 'user', 'content': query})
        # if not file:
        #     messages.append({'role': 'user', 'content': query})
        # else:
        #     messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})

        response = []
        for response in bot.run(messages):
            print('bot response:', response)
        logger.info(f'bot response: {response}')
        messages.extend(response)
        max_response_rounds-=1



if __name__ == '__main__':
    # ip =input("input ip:")
    # port =input("input port:")
    # testScan(ip,port)
    app_tui()
    