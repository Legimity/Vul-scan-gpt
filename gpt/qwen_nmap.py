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

# 可用
def nmapScan(
  ip: Optional[str],
  port: Optional[str],
    ) -> str:
  nm.scan(ip, port, arguments='"-Pn -T4 -sV -sT"')
  json_data = nm.analyse_nmap_xml_scan()
  scan_result = json_data["scan"]
  
  return scan_result

# test
def testScan(ip,port):   
    # print(f"'ip':{ip},'port':{port}")
    message_str = f"'role': 'user', 'content': 'Scanning the network for a given URL:{ip} and port :{port} and analyze the network state of the target.'"
    # str->dict, maybe there is a better way
    message_dict = ast.literal_eval("{" + message_str + "}")
    # print(message_dict)

    
    llm = get_chat_model({
        # Use the model service provided by DashScope:
        'model': 'qwen1.5-14b-chat',
        'model_server': 'dashscope',
        # 'api_key': os.getenv('DASHSCOPE_API_KEY'),
        'api_key': api_key,
    })

    # Step 1: send the conversation and available functions to the model
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
        # print(responses)
        last_response=responses
    print(last_response)

    messages.extend(responses)  # extend conversation with assistant's reply

    # Step 2: check if the model wanted to call a function
    last_response = messages[-1]
    if last_response.get('function_call', None):

        # Step 3: call the function
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
        # print('# Function Response:')
        # print("function_response",function_response)
        # print("messages",messages)
        # print("message.type",type(messages))

        # # Step 4: send the info for each function call and function response to the model
        messages.append({
            'role': 'function',
            'name': function_name,
            'content':  str(function_response),
        })  # extend conversation with function response

        # print("after messages",messages)

        print('# Assistant Response 2:')
        for responses in llm.chat(
                messages=messages,
                functions=functions,
                stream=True,
        ):  # get a new response from the model where it can see the function response
            # print(responses)
            last_response=responses
        print(last_response)


if __name__ == '__main__':
    ip =input("input ip:")
    port =input("input port:")
    testScan(ip,port)
    
    