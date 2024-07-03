# Reference: https://platform.openai.com/docs/guides/function-calling
import json
import os
from typing import Optional
import ast
import nmap
from qwen_agent.llm import get_chat_model
import dotenv
import os
dotenv.load_dotenv()

api_key=os.getenv('api_key')
nm = nmap.PortScanner()

# # Example dummy function hard coded to return the same weather
# # In production, this could be your backend API or an external API
# def get_current_weather(location, unit='fahrenheit'):
#     """Get the current weather in a given location"""
#     if 'tokyo' in location.lower():
#         return json.dumps({'location': 'Tokyo', 'temperature': '10', 'unit': 'celsius'})
#     elif 'san francisco' in location.lower():
#         return json.dumps({'location': 'San Francisco', 'temperature': '72', 'unit': 'fahrenheit'})
#     elif 'paris' in location.lower():
#         return json.dumps({'location': 'Paris', 'temperature': '22', 'unit': 'celsius'})
#     else:
#         return json.dumps({'location': location, 'temperature': 'unknown'})

# 可用
def nmapScan(
  ip: Optional[str],
  port: Optional[str],
    ) -> str:
  nm.scan(ip, port, arguments='"-Pn -T4 -sV -sT"')
  json_data = nm.analyse_nmap_xml_scan()
  scan_result = json_data["scan"]
  
  return scan_result


# def scan_website(url):
#     # 创建一个 PortScanner 对象
#     nm = nmap.PortScanner()
    
#     # 使用 nmap 对指定网址进行扫描
#     # 可以根据需要调整参数，例如更改 "-p" 参数以扫描特定端口范围
#     scan_result = nm.scan(url, arguments='-p 1-1024')
    
#     # 解析并打印扫描结果
#     print(f"Scanning report for {url}")
#     for host in nm.all_hosts():
#         print(f"Host: {host} ({nm[host].hostname()})")
#         print(f"State: {nm[host].state()}")
#         for proto in nm[host].all_protocols():
#             print(f"Protocol: {proto}")
#             lport = nm[host][proto].keys()
#             for port in lport:
#                 print(f"Port: {port}\tState: {nm[host][proto][port]['state']}")
                
#     return scan_result


def testScan(ip,port):
    # 输入：IP和port
    
    print(f"'ip':{ip},'port':{port}")
    
    message_str = f"'role': 'user', 'content': 'Scanning the network for a given URL:{ip} and port :{port} and analyze the network state of the target.'"
    # str->dict,maybe there is a better way
    message_dict = ast.literal_eval("{" + message_str + "}")

    print(message_dict)

    
    llm = get_chat_model({
        # Use the model service provided by DashScope:
        'model': 'qwen1.5-14b-chat',
        'model_server': 'dashscope',
        # 'api_key': os.getenv('DASHSCOPE_API_KEY'),
        'api_key': api_key,

        # Use the OpenAI-compatible model service provided by DashScope:
        # 'model': 'qwen1.5-14b-chat',
        # 'model_server': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        # 'api_key': os.getenv('DASHSCOPE_API_KEY'),

        # Use the model service provided by Together.AI:
        # 'model': 'Qwen/Qwen1.5-14B-Chat',
        # 'model_server': 'https://api.together.xyz',  # api_base
        # 'api_key': os.getenv('TOGETHER_API_KEY'),

        # Use your own model service compatible with OpenAI API:
        # 'model': 'Qwen/Qwen1.5-72B-Chat',
        # 'model_server': 'http://localhost:8000/v1',  # api_base
        # 'api_key': 'EMPTY',
    })

    # Step 1: send the conversation and available functions to the model
    # messages = [{'role': 'user', 'content': "Scanning the network for a given URL:127.0.0.1 and port 443 and analyze the network state of the target."}]
    messages = [message_dict]
    functions = [{
        'name': 'nmapScan',
        'description': 'Scanning the network for a given URL',
        'parameters': {
            'type': 'object',
            'properties': {
                'ip': {
                    'type': 'string',
                    'description': 'the ip of the target',
                },
                'port': {
                    'type': 'string',
                    'description': 'the port of the target',
                },
            },
            'required': ['ip','port'],
        },
    }]

    print('# Assistant Response 1:')
    responses = []



    for responses in llm.chat(
            messages=messages,
            functions=functions,
            stream=True,
            # Note: extra_generate_cfg is optional
            # extra_generate_cfg=dict(
            #     # Note: if function_choice='auto', let the model decide whether to call a function or not
            #     # function_choice='auto',  # 'auto' is the default if function_choice is not set
            #     # Note: set function_choice='get_current_weather' to force the model to call this function
            #     function_choice='get_current_weather',
            # ),
    ):
        # print("#########",responses)
        last_response=responses
    print(last_response)

    messages.extend(responses)  # extend conversation with assistant's reply

    # Step 2: check if the model wanted to call a function
    last_response = messages[-1]
    if last_response.get('function_call', None):

        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            'nmapScan': nmapScan,
        }  # only one function in this example, but you can have multiple
        function_name = last_response['function_call']['name']
        function_to_call = available_functions[function_name]
        function_args = json.loads(last_response['function_call']['arguments'])
        function_response = function_to_call(
            ip=function_args.get('ip'),
            port=function_args.get('port'),
        )
        print('# Function Response:')
        print("function_response",function_response)
        print("messages",messages)
        print("message.type",type(messages))

        # # Step 4: send the info for each function call and function response to the model
        messages.append({
            'role': 'function',
            'name': function_name,
            'content':  str(function_response),
        })  # extend conversation with function response

        print("after messages",messages)

        print('# Assistant Response 2:')
        for responses in llm.chat(
                messages=messages,
                functions=functions,
                stream=True,
        ):  # get a new response from the model where it can see the function response
            print(responses)
            # last_response=responses
        print(last_response)


if __name__ == '__main__':
    # ip =input("input ip:")
    # port =input("input port:")
    ip ="127.0.0.1"
    port ="443"
    testScan(ip,port)
    # result=nmapScan('127.0.0.1', '443')
    # print(result)
    # ip =input("input ip:")
    # port =input("input port:")
    # print(f"'ip':{ip},'port':{port}")
    
    # message_str = f"'role': 'user', 'content': 'Scanning the network for a given URL:{ip} and port :{port} and analyze the network state of the target.'"

    # message_dict = ast.literal_eval("{" + message_str + "}")

    # print(message_dict)

    