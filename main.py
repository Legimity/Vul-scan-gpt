import sys
sys.path.append('webScan')

from webScan.web_scan import WebScan 
from gpt.analyzer import PortScanAnalyzer
from portScan.port_scan import PortScanner,nmapScanner
from softwareScan.software_scan import SoftwareScanner
import argparse
from utils.logger import ColoredLogger
from utils.banner import banner
import subprocess
import time
print(banner())


# 配置日志记录器
logger = ColoredLogger().get_logger()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A vulnerability scanning tool combined with artificial intelligence for Xin-Chuang"
    )
    parser.add_argument("-ip","--ip", type=str, help="Target IP", required=True)
    parser.add_argument("-p", "--port", type=str, help="Target Port", required=True)
    parser.add_argument(
        "--choice",
        type=int,
        default=3,
        help="Enter choice of nmap scan (1-5):\n\
        1: Host Discover (-sP -T4) - Only performs host discovery\n \
        2: TCP SYN Scan (-Pn -sV -T4 -sS) - Recommended, most common, requires root\n\
        3: TCP Connect() Scan (-Pn -T4 -sV -sT) - Uses system call, full TCP connection, will be logged\n\
        4: UDP Scan (-Pn -sV -T4 -sU) - Probes UDP services, very slow, not recommended, requires root\n\
        5: TCP ACK Scan (-Pn -sV -T4 -sA) - Cannot detect open ports, used to check firewall rules, requires root\n",
    )
    # parser.add_argument('--analyzer', type=str, help='Llm for analyzing the result of the scan')

    return parser.parse_args()


def main():
    # parse arguments
    args = parse_arguments()
    ip = args.ip
    port = args.port

    
    # Nmap port scan 端口扫描with gpt
    # logger.info("Starting Nmap port scan...")
    # port_scan = PortScanner()
    # analyzer = PortScanAnalyzer()
    # response = port_scan.scanner(args.ip, args.port, args.choice, analyzer)
    # print(response)

    # Test nmap scan without gpt
    # logger.info("Starting Nmap port scan...")
    # nmap_scan = nmapScanner()
    # nmap_result = nmap_scan.run(ip=args.ip, port=args.port)
    # print(nmap_result)

    # Test webScan
    logger.info("Starting Web scan...")
    target_url = f'{args.ip}:{args.port}'
    logger.info("{}".format(target_url))

    try:
        webscan_result = WebScan(target_url=target_url).run()
        print(webscan_result)
    except Exception as e:
        logger.error(f"Error occurred during web scan: {str(e)}")
        webscan_result = None
    # TODO: 这里应该返回了webScan的扫描结果，需要进一步交给gpt处理
    print(webscan_result)


    # # 使用 subprocess 执行多条命令
    # # command = 'echo Hello && python webScan\web_scan.py'
    # # result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    # # print(result.stdout.decode())

    
    # # nikto software-vul scan
    # logger.info("Starting Nikto software scan...")
    # start_time = time.time()
    # softwareScanner = SoftwareScanner(target_url=ip,target_port=port)
    # to_be_analyse_by_gpt = softwareScanner.run()
    # end_time = time.time()
    # execution_time = end_time - start_time
    # # time count, nikto may cost many time i'm afraid
    # logger.info(f"Execution time: {execution_time} seconds")
    # # TODO：这里返回了nikto的扫描结果，需要进一步交给gpt处理
    # print(to_be_analyse_by_gpt)


if __name__ == "__main__":
    main()
