from nmap import PortScannerHostDict
import nmap

nm = nmap.PortScanner()

"""
DataProcessor: 数据处理类，提供对各种扫描结果对处理，处理完之后的数据用作大模型的输入
"""
class DataProcessor:
    """
    process_nmap_result: 处理nmap扫描结果
    """
    @staticmethod
    def process_nmap_result(nmap_result: dict[str, PortScannerHostDict]):
        extracted_data = {}
        for ip, details in nmap_result.items():
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

        return analyze_data
