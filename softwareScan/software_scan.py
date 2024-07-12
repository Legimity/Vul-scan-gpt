import subprocess
import logging
import os
import configparser
import uuid
import json
import sys
sys.path.append('./')
from utils.logger import ColoredLogger
logger=ColoredLogger().get_logger()

class SoftwareScanner:
    # nikto_path = "./nikto/program/nikto.pl"
    
    
    def __init__(self,target_url,target_port,targe_file=None):
            self.target_url = target_url
            self.target_port=target_port
            
            # 读取配置文件
            config = configparser.ConfigParser()
            config.read("./conf/conf.ini")
            self.save_path = config.get("save","save_path")
            self.nikto_path=os.path.join(os.path.dirname(__file__), "nikto/program/nikto.pl")
            self.output_path = self.save_path + "Nikto_" + uuid.uuid1().hex + ".json"
           
    # old api
    # 需要提供target
    def nikto_scanner(self, target, port):
        # 调用 Nikto 并捕获输出
        result = subprocess.run(
            ["perl", self.nikto_path, "-h", target,"-port",port,"-output",{self.save_path + "Nikto_" + uuid.uuid1().hex }],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.stderr:
            logging.error("Software scan Error:", result.stderr)
        else:
            with open(self.save_path + "Nikto_" + uuid.uuid1().hex + ".json","w") as result_file:
                json.dump(result.stdout, result_file, ensure_ascii=False)
            return result.stdout
        

    # new 需要提供target
    def run(self):
        # 调用 Nikto 并捕获输出
        # output_path = self.save_path + "Nikto_" + uuid.uuid1().hex + ".json"
        result = subprocess.run(
            [
              "perl", self.nikto_path,
              "-h", self.target_url,
              "-port",self.target_port,
              "-output",self.output_path,
              # "-Display","V"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.stderr:
            logging.error("Software scan Error:", result.stderr)
        else:
            # 读取上一步输出的文件
            with open(self.output_path, "r+") as result_file:
              result_data = result_file.read()

              # # 去除两端的中括号
              # result_data = result_data.strip("[]")
              # # 将文件指针移到文件开头
              # result_file.seek(0)
              # result_file.write(result_data)
              # result_file.truncate()
              
            
            return result_data
            # return result.stdout


if __name__ == "__main__":
    path=os.path.join(os.path.dirname(__file__), "nikto/program/nikto.pl")
    print(f"path: {path}")
    # scanner = SoftwareScanner(target_url="http://127.0.0.1",target_port="8080").run()#ERROR: The -port option cannot be used with a full URI\n"
    result = SoftwareScanner(target_url="127.0.0.1",target_port="8080").run()
    print(result)