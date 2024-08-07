#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.vulmap.module.banner import banner
from lib.vulmap.module.install import require
require()
from lib.vulmap.module.allcheck import version_check
from lib.vulmap.module import globals
from lib.vulmap.module.argparse import arg
from lib.vulmap.module.license import vulmap_license
from lib.vulmap.core.core import core
from lib.vulmap.module.time import now
from lib.vulmap.module.color import color
from lib.vulmap.thirdparty import urllib3
urllib3.disable_warnings()


def config(args):
    header = {
        'Accept': 'application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, '
                  'application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
        'User-agent': args.ua,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close'
    }
    globals.init()  # 初始化全局变量模块
    globals.set_value("UA", args.ua)  # 设置全局变量UA
    globals.set_value("VUL", None)  # 设置全局变量VULN用于判断是否漏洞利用模式
    globals.set_value("CHECK", args.check)  # 目标存活检测
    globals.set_value("DEBUG", args.debug)  # 设置全局变量DEBUG
    globals.set_value("DELAY", args.delay)  # 设置全局变量延时时间DELAY
    globals.set_value("DNSLOG", args.dnslog)  # 用于判断使用哪个dnslog平台
    globals.set_value("DISMAP", "flase") # 是否接收dismap识别结果(false/true)
    globals.set_value("VULMAP", str(0.9))  # 设置全局变量程序版本号
    globals.set_value("O_TEXT", args.O_TEXT)  # 设置全局变量OUTPUT判断是否输出TEXT
    globals.set_value("O_JSON", args.O_JSON)  # 设置全局变量OUTPUT判断是否输出JSON
    globals.set_value("HEADERS", header)  # 设置全局变量HEADERS
    globals.set_value("TIMEOUT", args.TIMEOUT)  # 设置全局变量超时时间TOMEOUT
    globals.set_value("THREADNUM", args.thread_num)  # 设置全局变量THREADNUM传递线程数量

    # 替换自己的 ceye.io 的域名和 token
    globals.set_value("ceye_domain","xxxxxxxxxx")
    globals.set_value("ceye_token", "xxxxxxxxxx")

    # 替换自己的 http://hyuga.co 的域名和 token
    # hyuga的域名和token可写可不写，如果不写则自动获得
    globals.set_value("hyuga_domain", "xxxxxxxxxx")
    globals.set_value("hyuga_token", "xxxxxxxxxx")

    # fofa 邮箱和 key，需要手动修改为自己的
    globals.set_value("fofa_email", "xxxxxxxxxx")
    globals.set_value("fofa_key", "xxxxxxxxxx")

    # shodan key
    globals.set_value("shodan_key", "xxxxxxxxxx")


class vulmapScan:
    def run(self,target_url):
        try:
            args = arg(target_url)  # 初始化各选项参数
            config(args)  # 加载全局变量
            core.control_options(args)  # 运行核心选项控制方法用于处理不同选项并开始扫描
        except KeyboardInterrupt as e:
            print(now.timed(de=0) + color.red_warn() + color.red(" Stop scanning"))
            exit(0)
