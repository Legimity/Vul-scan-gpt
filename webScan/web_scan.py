from webScan.lib.TPscan import TPscan
from webScan.lib.vulmap import Scan as vulmapscan  # 做了修改
from webScan.lib.struct2Scan import Struct2Scan


class WebScanner:
    def __init__(self, target_url):
        self.target_url = target_url

    def runWebScan(self):
        print("----加载TPscan----")
        tpScanResult = TPscan.Scan().run(self.target_url)
        ##TODO 修改bug

        print("----加载Vulmap----")
        vulmapscan.Scan().run(self.target_url)

        print("----加载Struct2Scan----")
        Struct2Scan.Scan().run(self.target_url)

        # TODO: 应该把三个结果结合返回给main.py
        return tpScanResult


if __name__ == "__main__":
    WebScanner("http://127.0.0.1:801").runWebScan()
