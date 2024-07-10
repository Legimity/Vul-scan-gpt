import json
from lib.vulmap import  vulmapScan
from lib.TPscan.TPscan import Scan 
import contextlib
import configparser
import uuid
import io
from utils.remove_ansi import remove_ansi_escape_sequences
class WebScan:
    def __init__(self,target_url):
        self.target_url = target_url
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read("./conf/conf.ini")
        self.save_path = config.get("save","save_path")
        print(self.save_path)

    def TPscan(self) -> dict:
        try:
            tpscan_output = Scan().run(self.target_url)
            print(f"{tpscan_output}")
        except Exception as e:
            print(f"Error occurred during TPscan: {str(e)}")
        with open(self.save_path + "TPScan_" + uuid.uuid1().hex + ".json","w") as result_file:
            json.dump(tpscan_output,result_file)
        return tpscan_output

    def run(self):
        result=''
        # TPscan 扫描
        tpscan_output = self.TPscan()
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

        print("----加载Struct2Scan----")
        from lib.struct2Scan import Struct2Scan    
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            Struct2Scan.Scan().run(self.target_url)
        struc2scan_output = f.getvalue()
        with open(self.save_path + "Struct2Scan" + uuid.uuid1().hex + ".json","w") as result_file:
            result_file.write(struc2scan_output)


        # print(type(output1),type(output2),type(output3))
        result=f'tpscan_output is :{tpscan_output}\n vulmap_output is :{vulmap_output}\n struc2scan_output is:{struc2scan_output}'
        # result=f'\n vulmap_output is :{vulmap_output}\n struc2scan_output is:{struc2scan_output}'
        '''
        print(tpscan_output)
        return result

if __name__=="__main__":  
#     # WebScan("http://127.0.0.1:8080").run() #禅道
#     # WebScan("http://127.0.0.1:8081").run() #帝国
      result=WebScan("http://127.0.0.1:8082").run() #织梦
      WebScan("http://tp5.test.com:80").run()
    # res = Scan().run("http://tp5.test.com:80")  # NOT OK
    # print(res)



