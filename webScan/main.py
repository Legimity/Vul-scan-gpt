from lib.TPscan import TPscan
from lib.vulmap import  vulmapScan
from lib.struct2Scan import Struct2Scan
import contextlib
import io
class WebScan:
    def __init__(self,target_url):
        self.target_url=target_url
    def run(self):
        print("----加载TPscan----")
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            TPscan.Scan().run(self.target_url)
        output = f.getvalue()
        with open("result/TPscan.txt","w") as result_file:
            result_file.write(output)

        print("----加载Vulmap----")
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            vulmapScan().run(self.target_url)
        output = f.getvalue()
        with open("result/Vulmap.txt","w",encoding="utf-8") as result_file:
            result_file.write(output)

        print("----加载Struct2Scan----")
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            Struct2Scan.Scan().run(self.target_url)
        output = f.getvalue()
        with open("result/Struct2Scan.txt","w",encoding="utf-8") as result_file:
            result_file.write(output)
WebScan("http://127.0.0.1:801").run()
