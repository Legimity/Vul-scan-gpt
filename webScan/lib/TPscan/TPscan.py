#!/usr/bin/env python
# coding=utf-8
from gevent import monkey
import sys
sys.path.append('webScan')

monkey.patch_all()
from gevent.pool import Pool
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

import gevent

class Scan:
    def run(self, targeturl):
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

    def pocexec(self, pocstr):
        pocdict = eval(pocstr)
        gevent.sleep(0)
        return pocdict

# if __name__ == "__main__":
# #     # res = Scan().run("http://127.0.0.1:80/tp5/public/index.php") #ok
# #     # res = Scan().run("http://127.0.0.1:80/tp5/public/") # ok
#     res = Scan().run("http://tp5.test.com:80")  # NOT OK
#     print(res)