import sys

sys.path.append('./')

from typing import Optional
from gpt.analyzer import PortScanAnalyzer
from utils.data_processor import DataProcessor
import uuid
import json
import configparser
from utils.logger import ColoredLogger
logger = ColoredLogger().get_logger()
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


class nmapScanner():
  def __init__(self,target_ip,target_port,targe_file=None)->None:
        self.target_ip = target_ip
        self.target_port=target_port
        # 读取配置文件
        config = configparser.ConfigParser(comment_prefixes="#")
        config.read("./conf/conf.ini")
        self.save_path = config.get("save","save_path")
        
  # 只需要传递ip
  def run(self) -> str:
      
      # 只进行主机发现（ping 扫描）查询主机是否在线
      nm.scan(hosts=self.target_ip, arguments='-sn')
      host=self.target_ip
      if host not in nm.all_hosts():
          return {"host": host, "state": "down", "open_ports": []}
      
      # 进行端口扫描
      nm.scan(hosts=host, arguments='-p 1-65535')
      
      host_info = {
          'host': host,
          'state': nm[host].state(),
          'addresses': nm[host].all_protocols(),
          'open_ports': []
      }

      for proto in nm[host].all_protocols():
          lport = nm[host][proto].keys()
          for port in lport:
              if nm[host][proto][port]['state'] == 'open':
                  host_info['open_ports'].append({
                      'port': port,
                      'protocol': proto,
                      'service': nm[host][proto][port]['name']
                  })
      host_info = [host_info]
      with open(self.save_path + "Nmap_" + uuid.uuid1().hex + ".json","w") as result_file:   
          json.dump(host_info,result_file)
      return host_info
  
  #需要ip和port  
  def certainPortscan(self):
          # Your code here to perform the nmap scan
      nm.scan(self.target_ip, self.target_port, arguments='"-Pn -T4 -sV -sT"')
      # nm.scan(self.target_ip,arguments="-sP -T4")
      json_data = nm.analyse_nmap_xml_scan()
      scan_result = json_data["scan"]
      # logger.info(f"Scanning the network for a given URL:{ip} and port :{port}.")
      return scan_result
      # return "the host is up and port is open"


if __name__ == "__main__":
    nmapscan=nmapScanner(target_ip="127.0.0.1",target_port="8080")
    result=nmapscan.run()
    print(result)