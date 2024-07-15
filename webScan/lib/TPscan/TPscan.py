import sys
sys.path.append('./')
sys.path.append('webScan')
from concurrent import futures
from utils.logger import ColoredLogger
import gevent
from gevent.pool import Pool
import json
import os

from lib.TPscan.plugins.thinkphp_checkcode_time_sqli import (
    thinkphp_checkcode_time_sqli_verify,
)
from lib.TPscan.plugins.thinkphp_construct_code_exec import (
    thinkphp_construct_code_exec_verify,
)
from lib.TPscan.plugins.thinkphp_construct_debug_rce import (
    thinkphp_construct_debug_rce_verify,
)
from lib.TPscan.plugins.thinkphp_debug_index_ids_sqli import (
    thinkphp_debug_index_ids_sqli_verify,
)
from lib.TPscan.plugins.thinkphp_driver_display_rce import (
    thinkphp_driver_display_rce_verify,
)
from lib.TPscan.plugins.thinkphp_index_construct_rce import (
    thinkphp_index_construct_rce_verify,
)
from lib.TPscan.plugins.thinkphp_index_showid_rce import (
    thinkphp_index_showid_rce_verify,
)
from lib.TPscan.plugins.thinkphp_invoke_func_code_exec import (
    thinkphp_invoke_func_code_exec_verify,
)
from lib.TPscan.plugins.thinkphp_lite_code_exec import (
    thinkphp_lite_code_exec_verify,
)
from lib.TPscan.plugins.thinkphp_method_filter_code_exec import (
    thinkphp_method_filter_code_exec_verify,
)
from lib.TPscan.plugins.thinkphp_multi_sql_leak import (
    thinkphp_multi_sql_leak_verify,
)
from lib.TPscan.plugins.thinkphp_pay_orderid_sqli import (
    thinkphp_pay_orderid_sqli_verify,
)
from lib.TPscan.plugins.thinkphp_request_input_rce import (
    thinkphp_request_input_rce_verify,
)
from lib.TPscan.plugins.thinkphp_view_recent_xff_sqli import (
    thinkphp_view_recent_xff_sqli_verify,
)

def check_file(file_path):
    """检查文件是否存在"""
    if os.path.exists(file_path):
        return True
    else:
        print(f"[-] {file_path} not found")
        exit(0)

def read_urls(file):
    """读取URL文件"""
    if check_file(file):
        with open(file, 'r') as f:
            serach_results = json.load(f)['results']
        urls = [res['url'] for res in serach_results]
        return urls



class Scan:
    def scan_more(self, targeturl):
        """批量扫描URL"""
        with futures.ProcessPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.scan_one, targeturl))
        return results[0]
    
    def scan_one(self, targeturl):
        if targeturl.find("http") == -1:
            exit(1)
        poclist = [
            'thinkphp_checkcode_time_sqli_verify("{0}")'.format(targeturl),
            'thinkphp_construct_code_exec_verify("{0}")'.format(targeturl),
            'thinkphp_construct_debug_rce_verify("{0}")'.format(targeturl),
            'thinkphp_debug_index_ids_sqli_verify("{0}")'.format(targeturl),
            'thinkphp_driver_display_rce_verify("{0}")'.format(targeturl),
            'thinkphp_index_construct_rce_verify("{0}")'.format(targeturl),
            'thinkphp_index_showid_rce_verify("{0}")'.format(targeturl),
            'thinkphp_invoke_func_code_exec_verify("{0}")'.format(targeturl),
            'thinkphp_lite_code_exec_verify("{0}")'.format(targeturl),
            'thinkphp_method_filter_code_exec_verify("{0}")'.format(targeturl),
            'thinkphp_multi_sql_leak_verify("{0}")'.format(targeturl),
            'thinkphp_pay_orderid_sqli_verify("{0}")'.format(targeturl),
            'thinkphp_request_input_rce_verify("{0}")'.format(targeturl),
            'thinkphp_view_recent_xff_sqli_verify("{0}")'.format(targeturl),
        ]
        pool = Pool(10)
        threads = [pool.spawn(self.pocexec, item) for item in poclist]
        gevent.joinall(threads)
        tpscan_output = [{
            "vulnname":thread.value["vulnname"],
            "isvul":thread.value["isvul"],
            "vulnurl":thread.value["vulnurl"],
            "payload":thread.value["payload"],
            "proof":thread.value["proof"]
            } for thread in threads if thread.value != None]
        return tpscan_output
    
    def run(self,url = None ,file = None) -> dict :
        result = None
        if url != None:
            result = self.scan_one(url)
        if file != None:
            urls = read_urls(file)
            file_res = self.scan_more(urls)
            result.extend(file_res)
        return result

    def pocexec(self, pocstr):
        pocdict = eval(pocstr)
        gevent.sleep(0)
        return pocdict
