import requests
import json
import re
from typing import Any


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
            "survival host" [""],
            "os information": [""], 
            "open ports": [""],
            "open services": [""],
            "found cve": [""]
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
        response = nmap_result_process(response)
        return response


def nmap_result_process(json_string: str) -> Any:
    survival_host_pattern = r'"survival host": \["(.*?)"\]'
    os_information_pattern = r'"os information": \["(.*?)"\]'
    open_ports_pattern = r'"open ports": \["(.*?)"\]'
    open_services_pattern = r'"open services": \["(.*?)"\]'
    found_cve_pattern = r'"found cve": \["(.*?)"\]'

    survival_host = None
    os_information = None
    open_ports = None
    open_services = None
    found_cve = None

    match = re.search(survival_host_pattern, json_string)
    if match:
        survival_host = match.group(1)
    match = re.search(os_information_pattern, json_string)
    if match:
        os_information = match.group(1)
    match = re.search(open_ports_pattern, json_string)
    if match:
        open_ports = match.group(1)
    match = re.search(open_services_pattern, json_string)
    if match:
        open_services = match.group(1)
    match = re.search(found_cve_pattern, json_string)
    if match:
        found_cve = match.group(1)

    # Create a dictionary to store the extracted data
    data = {
        "survival host": survival_host,
        "os information": os_information,
        "open ports": open_ports,
        "open services": open_services,
        "found cve": found_cve
    }

    json_output = json.dumps(data)

    return json_output
