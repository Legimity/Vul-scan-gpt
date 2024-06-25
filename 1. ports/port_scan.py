from typing import Optional
from analyzer import PortScanAnalyzer
import nmap


nm = nmap.PortScanner()
analyzer = PortScanAnalyzer()


class PortScanner:
    profile_arguments = {
        # 1、3、4 需要root权限
        1: '-Pn -sV -T4 -sS',    # TCP SYN 扫描   推荐，最常用
        2: '-T4 -sT',    # TCP Connect()扫描 # Connect()属于系统调用，属于TCP全连接，会被记录
        3: '-Pn -sV -T4 -sU',    # UDP扫描，探测建立在UDP协议上的服务，速度很慢，不推荐
        4: '-Pn -sV -T4 -sA',    # TCP ACK扫描，不能检测端口是否开放，但是可以用来检测防火墙规则
        5: '-sn -T4',    # 只进行主机发现
    }

    def scanner(self, ip: Optional[str], port: Optional[str], profile: int, analyzer: PortScanAnalyzer) -> str:
        nm.scan(ip, port, arguments=self.profile_arguments.get(profile))
        json_data = nm.analyse_nmap_xml_scan()
        scan_result = json_data["scan"]

        extracted_data = {}
        for ip, details in scan_result.items():
            open_ports = {}
            for port, port_details in details.get('tcp', {}).items():
                if port_details['state'] == 'open':
                    open_ports[port] = {
                        'service': port_details['name'],
                        'product': port_details['product'],
                        'version': port_details['version']
                    }
            if open_ports:
                extracted_data[ip] = open_ports

        analyze_data = {"nmap_command": nm.command_line(),
                        "nmap_scan_result": extracted_data}

        response = analyzer.llama(str(analyze_data))
        return response

    # TODO:
    # def scan_result_process(self):


