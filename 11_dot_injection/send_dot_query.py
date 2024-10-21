import socket
import ssl
import dns.message
import dns.query
import dns.rcode
import argparse
import ipaddress

def do53_query(name,type):
    query = dns.message.make_query(qname=name, rdtype=type)
    response_message = dns.query.udp(q=query, port=53, where='127.0.0.54', timeout=5)
    print(f'本地do53解析域名{name}的{type}记录:\n{response_message}')


def p1(dot,mode,name,type):
    print(f'========Phase 1: 解析获取DoT服务器的IP地址========')
    query = dns.message.make_query(qname=dot, rdtype='A')
    for i in range(1,4):
        try:
            response_message = dns.query.udp(q=query, port=53, where='127.0.0.54', timeout=5)
        except:
            response_message = ''
            print(f'获取失败，重试{i}')
    if response_message != '':
        print(f'{dot} A 记录地址为 {response_message.answer[0]}')
        p2(str(response_message.answer[0]).split(' ')[-1],args.mode,args.name,args.type)
    else:
        if mode == 'opportunistic':
            print('机会隐私设置，降为明文进行查询')
            do53_query(name, type)
        else:
            print('严格隐私设置，查询结束')


def p2(dot_ip,mode,name,type):
    print(f'========Phase 2: 与DoT服务器{dot_ip}建立连接========')
    query = dns.message.make_query(qname=name, rdtype=type)
    for i in range(1,4):
        try:
            response_message = dns.query.tls(q=query, port=853, where=dot_ip, timeout=5,verify=True)
        except:
            response_message = ''
            print(f'获取失败，重试{i}')
    if response_message == '':
        if mode == 'opportunistic':
            print('机会隐私设置，降为明文进行查询')
            do53_query(name, type)
        else:
            print('严格隐私设置，查询结束')
    else:
        print(f'解析域名{name}的{type}记录:\n{response_message}')



parser = argparse.ArgumentParser()
parser.add_argument('-dot', '--dot', default='dns.alidns.com')
parser.add_argument('-mode', '--mode', default='opportunistic')
parser.add_argument('-name', '--name', default='www.baidu.com')
parser.add_argument('-type', '--type', default='A')
args = parser.parse_args()

print(f'DoT server: {args.dot}')
try:
    if ipaddress.ip_address(args.dot):
        p2(args.dot, args.mode, args.name, args.type)

except:
    p1(args.dot,args.mode,args.name,args.type)
