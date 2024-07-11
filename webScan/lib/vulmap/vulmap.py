from lib.vulmap.module.banner import banner
from lib.vulmap.module.install import require
require()
from lib.vulmap.module.allcheck import version_check
from lib.vulmap.module import globals
from lib.vulmap.module.argparse import arg
from lib.vulmap.core.core import core
from lib.vulmap.module.time import now
from lib.vulmap.module.color import color
from lib.vulmap.thirdparty import urllib3
urllib3.disable_warnings()

from typing import List, Optional, Union

class VulmapArgs:
    """modify the arguments of vulmap"""
    def __init__(self,
                 url: Optional[str] = None,
                 file: Optional[str] = None,
                 fofa: Optional[str] = None,
                 shodan: Optional[str] = None,
                 app: str = None,
                 thread_num: int = 10,
                 dnslog: str = 'auto',
                 output_text: Optional[str] = None,
                 output_json: Optional[str] = None,
                 socks: Optional[str] = None,
                 http: Optional[str] = None,
                 size: int = 100,
                 user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                 delay: int = 0,
                 timeout: int = 10,
                 list_vulns: bool = True,
                 debug: bool = True,
                 check: str = 'on',
                 vuln_types: Optional[List[str]] = None):
        self.url = url
        self.file = file
        self.fofa = fofa
        self.shodan = shodan
        self.app = app
        self.thread_num = thread_num
        self.dnslog = dnslog
        self.O_TEXT = output_text
        self.O_JSON = output_json
        self.socks = socks
        self.http = http
        self.size = size
        self.ua = user_agent
        self.delay = delay
        self.TIMEOUT = timeout
        self.list = list_vulns
        self.debug = debug
        self.check = check
        self.vuln_types = vuln_types if vuln_types is not None else []

class Scan:
    def __init__(self) -> None:
        self.args = VulmapArgs()  # 初始化各选项参数
        header = {
            'Accept': 'application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, '
                    'application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
            'User-agent': self.args.ua,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'close'
        }
        globals.init()  # 初始化全局变量模块
        globals.set_value("UA", self.args.ua)  # 设置全局变量UA
        globals.set_value("VUL", None)  # 设置全局变量VULN用于判断是否漏洞利用模式
        globals.set_value("CHECK", self.args.check)  # 目标存活检测
        globals.set_value("DEBUG", self.args.debug)  # 设置全局变量DEBUG
        globals.set_value("DELAY", self.args.delay)  # 设置全局变量延时时间DELAY
        globals.set_value("DNSLOG", self.args.dnslog)  # 用于判断使用哪个dnslog平台
        globals.set_value("DISMAP", "flase") # 是否接收dismap识别结果(false/true)
        globals.set_value("VULMAP", str(0.9))  # 设置全局变量程序版本号
        globals.set_value("O_TEXT", self.args.O_TEXT)  # 设置全局变量OUTPUT判断是否输出TEXT)  # 设置全局变量OUTPUT判断是否输出TEXT
        globals.set_value("O_JSON", self.args.O_JSON)  # 设置全局变量OUTPUT判断是否输出JSON
        globals.set_value("HEADERS", header)  # 设置全局变量HEADERS
        globals.set_value("TIMEOUT", self.args.TIMEOUT)  # 设置全局变量超时时间TOMEOUT
        globals.set_value("THREADNUM", self.args.thread_num)  # 设置全局变量THREADNUM传递线程数量

        # 借助全局变量保存扫描结果
        globals.set_value("RESULTS", [])

        # 替换自己的 ceye.io 的域名和 token
        globals.set_value("ceye_domain","s0899i.ceye.io")
        globals.set_value("ceye_token", "f158ffc056da7a2db5f1da61f0ba253a")

        # 替换自己的 http://hyuga.co 的域名和 token
        # hyuga的域名和token可写可不写，如果不写则自动获得
        globals.set_value("hyuga_domain", "xxxxxxxxxx")
        globals.set_value("hyuga_token", "xxxxxxxxxx")

        # fofa 邮箱和 key，需要手动修改为自己的
        globals.set_value("fofa_email", "om2bg0urzfyh727rrseztus2bxpe@open_wechat")
        globals.set_value("fofa_key", "6b96942f1eaf26309d3300ccc7902800")

        # shodan key
        globals.set_value("shodan_key", "vwUrlL9MR74Zzc6KvUIh2Xc4y46YcinF")

    def run(self, targeturl):
        if targeturl.find("http") == -1:
            exit(1)
        try:
            self.args.url = targeturl
            #version_check()  # 检查vulmap版本
            core.control_options(self.args)  # 运行核心选项控制方法用于处理不同选项并开始扫描
        except KeyboardInterrupt as e:
            print(now.timed(de=0) + color.red_warn() + color.red(" Stop scanning"))
            exit(0)

        return globals.get_value("RESULTS")

        #return vulmap_output