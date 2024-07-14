import dataclasses


@dataclasses.dataclass
class Prompt:
    user_prompt: str = "请你按照上述要求执行任务，并按照指定的response格式进行响应."

    base_prompt: str = """你是一名经验丰富的渗透测试专家，在该领域拥有广泛的经验。你持有多项知名认证，包括 
                          OSCP（Offensive Security Certified Professional）、CEH（Certified Ethical Hacker）和 
                          CISSP（Certified Information Systems Security Professional）。
                          你的专业领域包括网络安全、应用程序安全和漏洞评估。你熟练使用不同的漏洞扫描工具，可以从扫描结果中准确地分析出关键点。"""
    # TODO: 是否要告诉llm工具是什么
    # nmap_intro_prompt: str = """Nmap是一款...."""

    namp_prompt: str = """基于以下Nmap扫描结果，请提供详细的分析和建议：
                         1. 请你提取出存活的主机(state字段值为up)，开放的端口以及端口对应的服务和版本;
                         2. 针对开放端口对应的服务和版本，提供可能存在的漏洞;
                         Nmap扫描结果如下：{nmap_result}
                         你需要按照下面指定的格式进行响应：{nmap_response_format}
                         确保response可以由python的json.loads()方法正确解析
                         """

    struct2_prompt: str = """基于以下Struct2扫描结果，请提供详细的分析和建议：
                            1. 提取出存在的漏洞(isvul字段值为true，则说明漏洞存在），漏洞编号为vulnname字段的值;
                            2. 针对存在的漏洞，根据扫描结果中的提供的url,poc,payload字段，提供漏洞利用方法;
                            3. 针对存在的漏洞，根据漏洞编号，提供漏洞的详细描述;
                            4. 针对存在的漏洞，根据漏洞编号，提供漏洞的危害程度评估;  
                            5. 针对存在的漏洞，根据漏洞编号，提供漏洞的修复建议;
                            Struct2扫描结果如下：{struct2_result}
                            你需要按照下面指定的格式进行响应：{struct2_response_format}
                            确保response可以由python的json.loads()方法正确解析
                            """

    tpscan_prompt: str = """基于以下TPscan扫描结果，请提供详细的分析和建议：
                           1. 提取出存在的漏洞(isvul字段值为true，则说明漏洞存在），漏洞编号为vulnname字段的值;
                           2. 针对存在的漏洞，根据漏洞编号，提供漏洞的详细描述;
                           3. 针对存在的漏洞，根据漏洞编号，提供漏洞的危害程度评估;  
                           4. 针对存在的漏洞，根据漏洞编号，提供漏洞的修复建议;
                           TPscan扫描结果如下：{tpscan_result}
                           你需要按照下面指定的格式进行响应：{tpscan_response_format}
                           确保response可以由python的json.loads()方法正确解析
                           """

    vulmap_prompt: str = """基于以下Vulmap扫描结果，请提供详细的分析和建议：
                            1. 扫描结果中包含的是已经发现的漏洞，请你根据扫描结果中description字段和plugin字段的描述，提供漏洞的详细描述;
                            2. 提供漏洞的详细描述;
                            3. 提供漏洞的危害程度评估;
                            4. 提供漏洞的修复建议;
                            Vulmap扫描结果如下：{vulmap_result}
                            你需要按照下面指定的格式进行响应：{vulmap_response_format}
                            确保response可以由python的json.loads()方法正确解析
                            """

    nikto_prompt: str = """基于以下Nikto扫描结果，请提供详细的分析和建议：
                           1. 根据扫描结果中的host,ip,port,url字段，提取出完整的存在漏洞的url;
                           2. 根据提供的vulnerabilities字段，提供漏洞的详细描述; 
                           3. 针对存在的漏洞，根据漏洞编号，提供漏洞的危害程度评估;  
                           4. 针对存在的漏洞，根据漏洞编号，提供漏洞的修复建议;
                           Nikto扫描结果如下：{nikto_result}
                           你需要按照下面指定的格式进行响应：{nikto_response_format}
                           确保response可以由python的json.loads()方法正确解析
                           """
    final_report_prompt: str = """基于以下namp,tpscan,struct2scan,vulmap,nikto扫描结果，生成一份渗透测试报告：
    1、项目背景和范围说明：
      公司名称：XYZ Corp.
      网络范围：包括内部办公室网络和公共面向客户的网站（www.xyzcorp.com）。
    2、测试方法和工具：
     请使用表格的形式列出测试工具的名称和其用途说明，表格如下
     
    3、发现的漏洞和安全问题：
     根据提供的description字段和msg字段，提供漏洞的详细描述和存在的安全问题

    4、验证和复现：
     根据提供的method字段或者其余信息描述如何验证每个漏洞的存在以及如何复现漏洞。提供详细的步骤、工具和设置环境的说明，确保可重现性和准确性。

    5、风险评估和建议：
     根据提供的vuln_risk字段对每个漏洞进行风险评估，包括潜在的影响和可能的攻击路径。根据vuln_fix字段提供关于修复漏洞的具体建议和最佳实践策略。

    6、总结和建议：
    总结整体的渗透测试结果，提供关于系统安全状态的总体评估。包括改进安全措施的建议和策略，确保系统的安全性和稳定性。

    nmap扫描结果为: {nmap_result},
    tpscan扫描结果为: {tpscan_result},
    struct2scan扫描结果为: {struct2_result},
    vulmap扫描结果为: {vulmap_result},
    nikto扫描结果为: {nikto_result}
    """

    nmap_response_format: str = """
    {
        "host": "主机ip地址",
        "open_ports":
        {
            "port": "开放的端口",
            "service": "服务",
            "version": "版本",
            "maybe_vuln": "可能存在的漏洞"
        }
    }"""

    struct2_response_format: str = """
    {
        "vuln_name": "漏洞编号",
        "vuln_desc": "漏洞描述",
        "method": "漏洞利用方法,根据url,poc,payload字段提供漏洞利用方法",
        "vuln_risk": "漏洞风险评估",
        "vuln_fix": "漏洞修复建议"
    }"""

    tpscan_response_format: str = """
    {
        "vul_name":"漏洞名称",
        "vulnurl":"漏洞利用地址",
        "payload":"payload",
        "vuln_risk": "漏洞风险评估",
        "vuln_fix": "漏洞修复建议"
    }"""

    vulmap_response_format: str = """
    {
        "url": "漏洞url",
        "cve": "漏洞编号",
        "description": "漏洞描述",
        "payload": "payload",
        "vuln_risk": "漏洞风险评估",
        "vuln_fix": "漏洞修复建议"
    }"""

    nikto_response_format: str = """
    {
         "url": "漏洞地址，包括ip和端口，或者是域名",
         "vulnerabilities": [
              {
                 "id": "漏洞编号",
                 "msg": "漏洞描述",
                 "vuln_risk":"漏洞威胁等级",
                 "vuln_fix":"修复建议"
              },
         ]
    }"""


def gen_nmap_prompt(nmap_result) -> str:
    # prompt = Prompt()
    return Prompt.base_prompt + Prompt.namp_prompt.format(nmap_result=nmap_result,
                                                          nmap_response_format=Prompt.nmap_response_format)


def gen_struct2_prompt(struct2_result) -> str:
    return Prompt.base_prompt + Prompt.struct2_prompt.format(struct2_result=struct2_result,
                                                             struct2_response_format=Prompt.struct2_response_format)


def gen_tpscan_prompt(tpscan_result) -> str:
    return Prompt.base_prompt + Prompt.tpscan_prompt.format(tpscan_result=tpscan_result,
                                                            tpscan_response_format=Prompt.tpscan_response_format)


def gen_vulmap_prompt(vulmap_result) -> str:
    return Prompt.base_prompt + Prompt.vulmap_prompt.format(vulmap_result=vulmap_result,
                                                            vulmap_response_format=Prompt.vulmap_response_format)


def gen_nikto_prompt(nikto_result) -> str:
    return Prompt.base_prompt + Prompt.nikto_prompt.format(nikto_result=nikto_result,
                                                           nikto_response_format=Prompt.nikto_response_format)


def gen_all_prompt(nmap_result, tpscan_result, struct2_result, vulmap_result, nikto_result) -> str:
    return Prompt.final_report_prompt.format(nmap_result=nmap_result,
                                             tpscan_result=tpscan_result,
                                             struct2_result=struct2_result,
                                             vulmap_result=vulmap_result,
                                             nikto_result=nikto_result)
