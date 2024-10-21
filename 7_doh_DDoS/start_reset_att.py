import argparse
import os
import time
from logger_DoE import *

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', default=1)
args = parser.parse_args()

logger = InfoLogger(interval=1)
logger.log_info(LogLevel.INFO, "程序开始运行")

streams = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19,21,23,25,27,29,31]
for i in streams[:int(args.n)]:
    print(f"python3 cve44487.py -s {i}")
    #process = os.popen(f"python cve44487.py -s {i}")
#print(process.read())
#process.close()
logger.log_info(LogLevel.INFO, "程序结束运行")
logger.close()  # 关闭日志记录