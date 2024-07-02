from gpt.analyzer import PortScanAnalyzer
from portScan.port_scan import PortScanner
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A vulnerability scanning tool combined with artificial intelligence for Xin-Chuang')
    parser.add_argument('--ip', type=str, help='Target IP')
    parser.add_argument('--port', type=str, help='Target Port')
    parser.add_argument('--choice', type=int, default=3, help=(
        'Enter choice of scan (1-5):\n'
        '1: Host Discover (-sP -T4) - Only performs host discovery\n'
        '2: TCP SYN Scan (-Pn -sV -T4 -sS) - Recommended, most common, requires root\n'
        '3: TCP Connect() Scan (-Pn -T4 -sV -sT) - Uses system call, full TCP connection, will be logged\n'
        '4: UDP Scan (-Pn -sV -T4 -sU) - Probes UDP services, very slow, not recommended, requires root\n'
        '5: TCP ACK Scan (-Pn -sV -T4 -sA) - Cannot detect open ports, used to check firewall rules, requires root\n'
    ))
    # parser.add_argument('--analyzer', type=str, help='Llm for analyzing the result of the scan')

    return parser.parse_args()


def main():
    args = parse_arguments()
    port_scan = PortScanner()
    analyzer = PortScanAnalyzer()
    response = port_scan.scanner(args.ip, args.port, args.choice, analyzer)
    print(response)


if __name__ == '__main__':
    main()
