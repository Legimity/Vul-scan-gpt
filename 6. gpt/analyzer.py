import requests
import json


class PortScanAnalyzer:
    @staticmethod
    def llama(nmap_output: str):
        # 使用LocalAI本地部署，LocalAI api是OpenAI api的仿写
        # 实际的llama api不是以下模版
        url = "http://localhost:8080/v1/chat/completions"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": "Llama-3-8B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": f"""Do a NMAP scan analysis on the provided NMAP scan information
        The NMAP output must return in a JSON format according to the provided
        output format. The data must be accurate in regards towards a pentest report.
        The data must follow the following rules:
        1) The NMAP scans must be done from a pentester point of view
        2) The final output must be minimal according to the format given.
        3) The final output must be kept to a minimal.
        4) If a value not found in the scan just mention an empty string.
        5) Analyze everything even the smallest of data.
        6) Completely analyze the data provided and give a confirm answer using the output format.
        
        The output format:
        {{
            "Os Information": [""], 
            "Survival Host" [""],
            "Open Ports(Services)": [""],
            "Open Services": [""],
        }}
        
        NMAP Data to be analyzed: {nmap_output}
        """
                }
            ],
            "temperature": 1
        }

        # request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        response = response.json()['choices'][0]['message']['content']
        return response




    # def gpt(key: str, data: Any) -> str:
    #
    #     openai.api_key = key
    #     prompt = f"""
    #         Do a NMAP scan analysis on the provided NMAP scan information
    #         The NMAP output must return in a JSON format accorging to the provided
    #         output format. The data must be accurate in regards towards a pentest report.
    #         The data must follow the following rules:
    #         1) The NMAP scans must be done from a pentester point of view
    #         2) The final output must be minimal according to the format given.
    #         3) The final output must be kept to a minimal.
    #         4) If a value not found in the scan just mention an empty string.
    #         5) Analyze everything even the smallest of data.
    #         6) Completely analyze the data provided and give a confirm answer using the output format.
    #
    #         The output format:
    #         {{
    #             "critical score": [""],
    #             "os information": [""],
    #             "open ports": [""],
    #             "open services": [""],
    #             "vulnerable service": [""],
    #             "found cve": [""]
    #         }}
    #
    #         NMAP Data to be analyzed: {data}
    #         """
    #     # A structure for the request
    #     messages = [{"content": prompt, "role": "assistant"}]
    #     # A structure for the request
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=messages,
    #         max_tokens=2500,
    #         n=1,
    #         stop=None,
    #     )
    #     response = response['choices'][0]['message']['content']
    #     rsp = str(response)
    #     return str(nmap_ai_data_regex(rsp))