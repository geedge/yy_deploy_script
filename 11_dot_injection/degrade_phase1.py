import socket
import ssl
import dns.message
import dns.query
import dns.rcode
import argparse
from logger_DoE import *
import pandas as pd

domains = set(pd.read_csv('domains.csv').domain)

upstream_server = '223.5.5.5'

# 创建监听socket
listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listener.bind(('127.0.0.54', 53))

parser = argparse.ArgumentParser()
parser.add_argument('-pass', '--passdoe', default=0)
parser.add_argument('-tamper', '--tamper', default='')
parser.add_argument('-inject', '--inject', default='')
parser.add_argument('-ns', '--ns', default='1.1.1.1')
args = parser.parse_args()
tamper = args.tamper +'.'
inject = args.inject +'.'
ns = args.ns

logger = InfoLogger(interval=1)
logger.log_info(LogLevel.INFO, "程序开始运行")

while True:
    # 接收DNS请求
    data, addr = listener.recvfrom(1024)
    #print(dns.message.from_wire(data))
    data = dns.message.from_wire(data)
    query_r = data.question[0].name.to_text()[:-1]
    if query_r in domains and args.passdoe==0:
        # print(data.question[0].name.to_text()[:-1])
        # print(addr)
        #print(data)
        #print('对DoE域名的DNS请求：', query_r)
        logger = InfoLogger(interval=1)
        logger.log_info(LogLevel.INFO, f'对DoE域名的DNS请求：{query_r}')
        # # 创建TLS连接并发送DNS请求到上游服务器
        resp = dns.query.udp(
            q=data,
            where=upstream_server,
            timeout=10)
        #print('DNS响应：', resp.answer)
        resp.answer = [dns.rrset.from_text(query_r+'.', 3600, dns.rdataclass.IN, dns.rdatatype.A, '10.10.10.10')]
        #print(f'对DoE域名{query_r}的DNS请求已阻断，返回10.10.10.10')
        logger.log_info(LogLevel.INFO, f'对DoE域名{query_r}的DNS请求已阻断，返回10.10.10.10')
        logger.log_info(LogLevel.PAYLOAD, str(resp.answer.__str__()))
        # with socket.create_connection((upstream_server,853)) as sock:
        #     with context.wrap_socket(sock, server_hostname=upstream_server[0]) as tls_sock:
        #         tls_sock.sendall(data.to_wire())
        #         resp = tls_sock.recv(4096)

        # 将上游服务器的响应发送回客户端
        listener.sendto(resp.to_wire(), addr)
    else:
        resp = dns.query.udp(
            q=data,
            where=upstream_server,
            timeout=10)
        if str(resp.question[0].name) == tamper and int(resp.question[0].rdtype) == 1:
            print('---tamper---', tamper)
            resp.answer = [
                dns.rrset.from_text(tamper, 3600, dns.rdataclass.IN, dns.rdatatype.A, '8.8.8.8')]
        if str(resp.question[0].name) == inject:
            print('---inject---', inject)
            resp.additional = [
                dns.rrset.from_text(inject, 3600, dns.rdataclass.IN, dns.rdatatype.NS, 'ns.' + inject.split('.', 1)[1]),
                dns.rrset.from_text('ns.' + inject.split('.', 1)[1], 3600, dns.rdataclass.IN, dns.rdatatype.A, ns)]
        listener.sendto(resp.to_wire(), addr)
        #break
