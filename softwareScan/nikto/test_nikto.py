import subprocess
import time
import logging


# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_nikto(target):
    try:
        # 设置 Nikto 的路径
        # nikto_path = "./nikto/program/nikto .pl"
        nikto_path = "./program/nikto.pl"
        
        # 调用 Nikto 并捕获输出
        result = subprocess.run(
            # ['perl', nikto_path, '-h', target],
            ['perl', nikto_path, '-h', target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 检查是否有错误输出
        if result.stderr:
            print("Error:", result.stderr)
        else:
            # print("Nikto scan result:\n", result.stdout)
            with open('/disk2/lizw/nikto-master/scan_result.txt', 'w') as file:
                file.write(result.stdout)
                logging.info("Scan result saved to scan_result.txt")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    logging.info("Starting Nikto scan...")
    
    # 目标 URL 或 IP 地址
    # target = "http://example.com"
    # target = "127.0.0.1" 出错 80port not open
    target = "https://cyber.seu.edu.cn/"  #ok
    # target = "192.168.154.128" 虚拟机无法连接 
    
    
    # 运行 Nikto 扫描
    start_time = time.time()
    run_nikto(target)
    end_time = time.time()

    execution_time = end_time - start_time
    logging.info("Execution time: %s seconds", execution_time)
    # 将扫描结果保存到文件
    
      
    
