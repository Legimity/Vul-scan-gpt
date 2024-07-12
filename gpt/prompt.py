import dataclasses


@dataclasses.dataclass
class Prompt:
    base_prompt: str = """你是一名经验丰富的渗透测试专家，在该领域拥有广泛的经验。你持有多项知名认证，包括 
                          OSCP（Offensive Security Certified Professional）、CEH（Certified Ethical Hacker）和 
                          CISSP（Certified Information Systems Security Professional）。
                          你的专业领域包括网络安全、应用程序安全和漏洞评估。你熟练使用不同的漏洞扫描工具，可以从扫描结果中准确地分析出关键点。"""
    # TODO: 是否要告诉llm工具是什么
    # nmap_intro_prompt: str = """Nmap是一款...."""
    
    namp_prompt: str = """基于以下Nmap扫描结果，请提供详细的分析和建议：
                         1. 分析主机存活情况、开放端口、服务版本等信息;
                         Nmap扫描结果如下：{namp_result}"""

    struct2_prompt: str = """基于以下Struct2扫描结果，请提供详细的分析和建议：
                            1. 总结本次扫描中存在的漏洞，如果isvul为true，则说明漏洞存在，漏洞编号为vulnname字段的值;
                            2. 针对存在的漏洞，根据扫描结果中的提供的url,poc,payload字段，提供漏洞利用方法;
                            3. 针对存在的漏洞，根据漏洞编号，提供漏洞的详细描述;
                            4. 针对存在的漏洞，根据漏洞编号，提供漏洞的危害程度评估;  
                            5. 针对存在的漏洞，根据漏洞编号，提供漏洞的修复建议;
                            Struct2扫描结果如下：{struct2_result}"""

    tpscan_prompt: str = """基于以下TPscan扫描结果，请提供详细的分析和建议：
                           1. 总结本次扫描中存在的漏洞，如果isvul为true，则说明漏洞存在，漏洞编号为vulnname字段的值;
                           2. 针对存在的漏洞，根据漏洞编号，提供漏洞的详细描述;
                           3. 针对存在的漏洞，根据漏洞编号，提供漏洞的危害程度评估;  
                           4. 针对存在的漏洞，根据漏洞编号，提供漏洞的修复建议;
                           TPscan扫描结果如下：{tpscan_result}"""

    vulmap_prompt: str = """基于以下Vulmap扫描结果，请提供详细的分析和建议：
                            1. 扫描结果中包含的是已经发现的漏洞，请你根据扫描结果中description字段和plugin字段的描述，提供漏洞的详细描述;
                            2. 提供漏洞的详细描述;
                            3. 提供漏洞的危害程度评估;
                            4. 提供漏洞的修复建议;
                            Vulmap扫描结果如下：{vulmap_result}"""

    nikto_prompt: str = """基于以下Nikto扫描结果，请提供详细的分析和建议：
                           1. 根据扫描结果中的host,ip,port,vulnerabilities字段，划分出不同ip和端口的漏洞信息; 
                           2. 
                            """

    nmap_response_format: str = """
    response:
    [
        {
            "host": "主机ip地址"
            "open_ports":
            [
                {
                    "port": "开放的端口",
                    "service": "服务",
                    "version": "版本",
                    "maybe_vuln": "可能存在的漏洞"
                }
            ]
        }
    ]
    """

    struct2_response_format: str = """"""

    tpscan_response_format: str = """"""

    vulmap_response_format: str = """"""

    nikto_response_format: str = """"""


def gen_(task) -> str:
    prompt = Prompt()
