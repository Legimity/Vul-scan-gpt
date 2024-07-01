from module.banner import banner
print(banner())  # 显示随机banner
from module.install import require
require()
from module.allcheck import version_check
from module import globals
from module.argparse import arg
from module.license import vulmap_license
from core.core import core
from module.time import now
from module.color import color
from thirdparty import urllib3
from . import config

class Scan:
    def Scan(self):
        try:
            vulmap_license()  # vulmap 用户协议及免责声明
            args = arg()  # 初始化各选项参数
            config()  # 加载全局变量
            version_check()  # 检查vulmap版本
            core.control_options(args)  # 运行核心选项控制方法用于处理不同选项并开始扫描
        except KeyboardInterrupt as e:
            print(now.timed(de=0) + color.red_warn() + color.red(" Stop scanning"))
            exit(0)