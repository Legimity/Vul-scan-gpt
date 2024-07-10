import json
from lib.vulmap import  vulmapScan
from lib.TPscan.TPscan import Scan
# from lib.struct2Scan import Struct2Scan
import contextlib
import io

class WebScan:
    def __init__(self,target_url):
        self.target_url=target_url
        
    def run(self):
        result=''
        print("----加载TPscan----")
        try:
            tpscan_output = Scan().run(self.target_url)
            print(f"{tpscan_output}")
        except Exception as e:
            print(f"Error occurred during TPscan: {str(e)}")
        with open("result/TPscan.json","w") as result_file:
            json.dump(tpscan_output,result_file)
        # return
    
        print("----加载Vulmap----")
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            vulmapScan().run(self.target_url)
        vulmap_output = f.getvalue()
        with open("result/Vulmap.txt","w",encoding="utf-8") as result_file:
            result_file.write(vulmap_output)

        print("----加载Struct2Scan----")
        from lib.struct2Scan import Struct2Scan    
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            Struct2Scan.Scan().run(self.target_url)
        struc2scan_output = f.getvalue()
        with open("result/Struct2Scan.txt","w",encoding="utf-8") as result_file:
            result_file.write(struc2scan_output)


        # print(type(output1),type(output2),type(output3))
        result=f'tpscan_output is :{tpscan_output}\n vulmap_output is :{vulmap_output}\n struc2scan_output is:{struc2scan_output}'
        # result=f'\n vulmap_output is :{vulmap_output}\n struc2scan_output is:{struc2scan_output}'

        return result

if __name__=="__main__":  
#     # WebScan("http://127.0.0.1:8080").run() #禅道
#     # WebScan("http://127.0.0.1:8081").run() #帝国
#     result=WebScan("http://127.0.0.1:8082").run() #织梦
#     print(result)
      WebScan("http://tp5.test.com:80").run()
    # res = Scan().run("http://tp5.test.com:80")  # NOT OK
    # print(res)



