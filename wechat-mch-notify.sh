#!/bin/bash

# 使用curl请求web页面，然后使用grep和sed提取符合条件的字符串
strings=$(curl -s "https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncementlist" | grep -o 'e_id[^&]*&version' | sed 's/e_id=//; s/&version//')

# 固定字符串
fixed_string="https://mp.weixin.qq.com/cgi-bin/announce?action=getannouncement&announce_id="

days_ago=133
day_start=$(date "+%s" -d "$(date -d "${days_ago} days ago" "+%Y-%m-%d") 00:00:00")
day_end=$(date "+%s" -d "$(date -d "${days_ago} days ago" "+%Y-%m-%d") 23:59:59")

Z=""
# 对每个匹配的字符串进行处理并打印
for string in $strings
do
    specified_time=${string:1:10}
    processed_string="${fixed_string}${string}"
	if [ $specified_time -ge $day_start ] && [ $specified_time -le $day_end ]; then
	    echo "News: $processed_string"
        Z="${Z}News: $processed_string "
	fi
done

python send_mail.py WeChat-Mch-Notify "$Z"
