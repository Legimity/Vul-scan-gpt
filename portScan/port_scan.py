from typing import Optional
from gpt.analyzer import PortScanAnalyzer
from utils.data_processor import DataProcessor
import nmap

nm = nmap.PortScanner()
analyzer = PortScanAnalyzer()


class PortScanner:
    profile_arguments = {
        # Host Discover
        1: "-sP -T4",  # 只进行主机发现
        # 3: '',
        # 4: '',
        # 5: '',
        # Port Scan
        2: "-Pn -sV -T4 -sS",  # TCP SYN 扫描   推荐，最常用，需要root
        3: "-Pn -T4 -sV -sT",  # TCP Connect()扫描 # Connect()属于系统调用，属于TCP全连接，会被记录
        4: "-Pn -sV -T4 -sU",  # UDP扫描，探测建立在UDP协议上的服务，速度很慢，不推荐，需要root
        5: "-Pn -sV -T4 -sA",  # TCP ACK扫描，不能检测端口是否开放，但是可以用来检测防火墙规则，需要root
    }

    def scanner(
        self,
        ip: Optional[str],
        port: Optional[str],
        profile: int,
        analyzer: PortScanAnalyzer,
    ) -> str:
        nm.scan(ip, port, arguments=self.profile_arguments.get(profile))
        json_data = nm.analyse_nmap_xml_scan()
        scan_result = json_data["scan"]
        analyze_data = DataProcessor.process_nmap_result(scan_result)
        response = analyzer.llama(str(analyze_data))
        return response
