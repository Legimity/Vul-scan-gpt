import subprocess
import logging
import os

class SoftwareScanner:
    # nikto_path = "./nikto/program/nikto.pl"
    nikto_path=os.path.join(os.path.dirname(__file__), "nikto/program/nikto.pl")
    

    # 需要提供target
    def nikto_scanner(self, target,port ):
        # 调用 Nikto 并捕获输出
        result = subprocess.run(
            ["perl", self.nikto_path, "-h", target,"-port",port],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.stderr:
            logging.error("Software scan Error:", result.stderr)
        else:
            return result.stdout

if __name__ == "__main__":
    path=os.path.join(os.path.dirname(__file__), "nikto/program/nikto.pl")
    print(path)