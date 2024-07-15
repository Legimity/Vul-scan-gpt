import json
import sys
import importlib
import configparser
import uuid
import subprocess

sys.path.append('./')

from utils.remove_ansi import remove_ansi_escape_sequences
from utils.logger import ColoredLogger

logger = ColoredLogger().get_logger()

class WebScan:
    def __init__(self,target_url,targe_file=None):
        self.target_url = target_url
        self.dir_search_result = None
        # 读取配置文件
        config = configparser.ConfigParser(comment_prefixes="#")
        config.read("./conf/conf.ini")
        self.save_path = config.get("save","save_path")
        self.tp_scan = config.get("webScan","TPscan")
        self.struct2Scan = config.get("webScan","struct2Scan")
        self.vulmap = config.get("webScan","vulmap")
        self.dirScan = config.get("webScan","dirsearch")

    def dirsearch(self):
        self.dir_search_result = f"result/dirsearch/{uuid.uuid1().hex}.json"
        subprocess.run(["python",f"{self.dirScan}dirsearch.py","-u",self.target_url,"-e","php,action,html",
                        "-t","10",
                        "-r",
                        "-o",self.dir_search_result,
                        "-w",r"webScan\lib\dirsearch\db\vul-scan-gpt.txt",
                        "--format","json"])
        
        return self.dir_search_result
        

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
            struct2scan_outputs = Scan().run(self.target_url,self.dir_search_result)
            logger.info(f"struct2scan_output:\n")
            for idx, output in enumerate(struct2scan_outputs):
                logger.info(f"\n {idx}:\t url :{output['url']} \n\t vulnname:{output['vulnname']}\n\tpoc:{output['poc']}")
        except Exception as e:
            logger.error(f"Error occurred during Struct2Scan: {str(e)}")
        with open(self.save_path + "struct2Scan/struct2Scan_" + uuid.uuid1().hex + ".json","w") as result_file:
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
            header = None,shouldDirScan = False) -> dict :
        if shouldDirScan:
            self.dirsearch()
            struct2scan_output = self.Struct2Scan()
        else:
            struct2scan_output = self.Struct2Scan()
        # TPscan 扫描
        # tpscan_output = self.TPscan(self.target_url)
        # Struct2Scan 扫描
        # struct2scan_output = self.Struct2Scan(target_url=self.target_url,targe_file=self.dir_search_result)
        # Vulmap 扫描
        # vulmap_output = self.Vulmap()
        #print(vulmap_output)
        return struct2scan_output

if __name__=="__main__":  
    # test tpscan
    # WebScan("http://127.0.0.1:8080").run() #禅道
    # WebScan("http://127.0.0.1:8081").run() #帝国
    # result=WebScan("http://127.0.0.1:8082").run() #织梦
    
    # result=WebScan("http://tp5.test.com:80").run()
    result=WebScan("http://127.0.0.1:8080").run(shouldDirScan=True)

    # test struc2scan
    # result=WebScan("http://127.0.0.1:8080/login.action").run()
    # result=WebScan("localhost:8082/dede").run()
    # result=WebScan("localhost:8081/e/admin").run()
    
    
    # logger.info(result)

    # test vulmap
    # result=WebScan("http://127.0.0.1:8161/").run()
    # print(result)