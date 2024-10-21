# -*- coding: utf-8 -*-
import time
import json
import threading
from queue import Queue

class LogLevel:
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    PAYLOAD = "PAYLOAD"

class LogEntry:
    def __init__(self, log_level, log_info):
        self.created_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.log_level = log_level
        self.log_info = log_info

class InfoLogger:
    def __init__(self, interval=1):
        self.log_queue = Queue()
        self.interval = interval
        self.logging_thread = threading.Thread(target=self.start_logging)
        self.logging_thread.daemon = True
        self.logging_thread.start()

    def start_logging(self):
        while True:
            entry = self.log_queue.get()
            if entry is None:  # 退出信号
                break
            # time.sleep(self.interval)  # 延迟输出
            # 确保输出中文
            print(json.dumps(entry.__dict__, ensure_ascii=False))

    def log_info(self, level, message):
        entry = LogEntry(level, message)
        self.log_queue.put(entry)  # 将日志条目发送到队列

    def close(self):
        self.log_queue.put(None)  # 发送退出信号
        self.logging_thread.join()  # 等待线程结束

# 主函数
# if __name__ == "__main__":
#     logger = InfoLogger(interval=1)
#     logger.log_info(LogLevel.INFO, "程序开始运行")
#     logger.log_info(LogLevel.WARNING, "这是一个警告信息")
#     logger.log_info(LogLevel.ERROR, "发生了一个错误")
#     logger.log_info(LogLevel.PAYLOAD, "处理的有效负载信息")
#     logger.log_info(LogLevel.INFO, "程序结束运行")
#     logger.close()  # 关闭日志记录
