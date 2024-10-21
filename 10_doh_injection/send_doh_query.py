import socket
import ssl
import dns.message
import dns.query
import dns.rcode
import argparse
import ipaddress
import base64
import httpx


def do53_query(name,type):
    query = dns.message.make_query(qname=name, rdtype=type)
    response_message = dns.query.udp(q=query, port=53, where='127.0.0.54', timeout=5)
    print(f'本地do53解析域名{name}的{type}记录:\n{response_message}')


def p1(doh,mode,name,type):
    print(f'========Phase 1: 解析获取DoT服务器的IP地址========')
    query = dns.message.make_query(qname=doh, rdtype='A')
    for i in range(1,4):
        try:
            response_message = dns.query.udp(q=query, port=53, where='127.0.0.54', timeout=5)
        except:
            response_message = ''
            print(f'获取失败，重试{i}')
    if response_message != '':
        print(f'{doh} A 记录地址为 {response_message.answer[0]}')
        p2(str(response_message.answer[0]).split(' ')[-1],args.mode,args.name,args.type)
    else:
        if mode == 'opportunistic':
            print('机会隐私设置，降为明文进行查询')
            do53_query(name, type)
        else:
            print('严格隐私设置，查询结束')


def p2(doh_ip,mode,name,type):
    print(f'========Phase 2: 与DoT服务器{doh_ip}建立连接========')
    query = dns.message.make_query(qname=name, rdtype=type)
    headers = {"content-type": "application/dns-message", "accept": "application/dns-message", "host":doh_ip}
    for i in range(1,4):
        try:
            with httpx.Client(http2=True, http1=True, verify=True, timeout=5) as client:
                resp = client.get(f"https://{doh_ip}/dns-query?dns=" + base64.b64encode(query.to_wire()).decode("UTF8").rstrip("="),
                           headers=headers)
                response_message = dns.message.from_wire(resp.content)
                #print(response_message)

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
parser.add_argument('-doh', '--doh', default='dns.alidns.com')
parser.add_argument('-mode', '--mode', default='opportunistic')
parser.add_argument('-name', '--name', default='www.baidu.com')
parser.add_argument('-type', '--type', default='A')
args = parser.parse_args()

print(f'DoH server: {args.doh}')
try:
    if ipaddress.ip_address(args.doh):
        p2(args.doh, args.mode, args.name, args.type)

except:
    p1(args.doh,args.mode,args.name,args.type)
