import subprocess
import logging


class SoftwareScanner:
    nikto_path = "./nikto/program/nikto.pl"

    # 需要提供target
    def nikto_scanner(self, target):
        # 调用 Nikto 并捕获输出
        result = subprocess.run(
            ["perl", self.nikto_path, "-h", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.stderr:
            logging.error("Software scan Error:", result.stderr)
        else:
            return result.stdout
