from lib.TPscan import TPscan
from lib.vulmap import  vulmapscan
from lib.struct2Scan import Struct2Scan
class WebScan:
    def __init__(self,target_url):
        self.target_url=target_url
    def run(self):
        print("----加载TPscan----")
        TPscan.Scan().run(self.target_url)
        ##TODO 修改bug
        print("----加载Vulmap----")
        vulmapscan.Scan().run(self.target_url)
        print("----加载Struct2Scan----")
        Struct2Scan.Scan().run(self.target_url)


WebScan("http://127.0.0.1:801").run()
