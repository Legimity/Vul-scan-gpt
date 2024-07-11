import json
import sys
import importlib
import configparser
import uuid
import io
import os

sys.path.append('./')

from utils.remove_ansi import remove_ansi_escape_sequences
from utils.logger import ColoredLogger

logger = ColoredLogger().get_logger()

class WebScan:
    def __init__(self,target_url,targe_file=None):
        self.target_url = target_url
        # 读取配置文件
        config = configparser.ConfigParser(comment_prefixes="#")
        config.read("./conf/conf.ini")
        self.save_path = config.get("save","save_path")
        self.tp_scan = config.get("webScan","TPscan")
        self.struct2Scan = config.get("webScan","struct2Scan")
        self.vulmap = config.get("webScan","vulmap")

    def TPscan(self) -> dict:
        try:
            Scan = getattr(importlib.import_module(self.tp_scan),'Scan')
            tpscan_output = Scan().run(self.target_url)
            logger.info(f"tpscan_output:\n{tpscan_output}")
        except Exception as e:
            logger.error(f"Error occurred during TPscan: {str(e)}")
        with open(self.save_path + "TPScan_" + uuid.uuid1().hex + ".json","w") as result_file:
            json.dump(tpscan_output,result_file)
        return tpscan_output

    def Struct2Scan(self) -> dict:
        struct2scan_outputs = None
        try:
            Scan = getattr(importlib.import_module(self.struct2Scan),'Scan')
            struct2scan_outputs = Scan().run(self.target_url)
            # logger.info(f"struct2scan_output:\n")
            # for idx,output in enumerate(struct2scan_outputs):
            #     logger.info(f"\n {idx}:\turl :{output['url']} \n\tvulnname:{output['vulnname']}\n\tpoc:{output['poc']}")
        except Exception as e:
            logger.error(f"Error occurred during Struct2Scan: {str(e)}")
        with open(self.save_path + "Struct2Scan_" + uuid.uuid1().hex + ".json","w") as result_file:
            json.dump(struct2scan_outputs,result_file)
        return struct2scan_outputs

    def Vulmap(self) -> dict:
        try:
            Scan = getattr(importlib.import_module(self.vulmap),'Scan')
            vulmap_outputs = Scan().run(self.target_url)
            # logger.info(f"vulmap_output:\n{vulmap_output}")
        except Exception as e:
            logger.error(f"Error occurred during Vulmap: {str(e)}")
        with open(self.save_path + "Vulmap_" + uuid.uuid1().hex + ".json","w") as result_file:
            json.dump(vulmap_outputs, result_file, ensure_ascii=False)
        return vulmap_outputs

    def run(self,target_url=None,targe_file=None,data = None,
            header = None) -> dict :
        result=''
        # TPscan 扫描
        tpscan_output = self.TPscan()
        # Struct2Scan 扫描
        struct2scan_output = self.Struct2Scan()
        # Vulmap 扫描
        vulmap_output = self.Vulmap()
        #print(vulmap_output)

        '''
        print("----加载Vulmap----")
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            vulmapScan().run(self.target_url)
        vulmap_output = f.getvalue()
        # 处理vulmap的ansi输出
        # vulmap_output = remove_ansi_escape_sequences(vulmap_output)
        # with open("result/Vulmap.txt","w",encoding="utf-8") as result_file:
        with open(self.save_path + "Vulmap_" + uuid.uuid1().hex + ".json","w") as result_file:
            result_file.write(vulmap_output)

        # print(type(output1),type(output2),type(output3))
        result=f'tpscan_output is :{tpscan_output}\n vulmap_output is :{vulmap_output}\n struc2scan_output is:{struc2scan_output}'
        # result=f'\n vulmap_output is :{vulmap_output}\n struc2scan_output is:{struc2scan_output}'
        '''
        return result

if __name__=="__main__":
    # WebScan("http://127.0.0.1:8080").run() #禅道
    # WebScan("http://127.0.0.1:8081").run() #帝国
    # WebScan("http://127.0.0.1:8082").run() #织梦
    # WebScan("http://tp5.test.com:80").run()

    # 测试 struc2scan
    # WebScan("http://127.0.0.1:8080/login.action").run()
    # res = Scan().run("http://tp5.test.com:80")  # NOT OK
    # logger.info(result)

    # 测试 vulmap
    WebScan("http://127.0.0.1:8161/").run()