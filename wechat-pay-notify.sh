#!/bin/bash

# 发送curl请求获取JSON数据
response=$(curl -s "https://pay.weixin.qq.com/index.php/public/cms/get_contents?pagenum=1&id=6200&cmstype=1&url=https%253A%252F%252Fpay.weixin.qq.com%252Fpublic%252Fcms%252Fcontent_list%253Flang%253Dzh%2526id%253D6200&field=contentId%2CcontentTitle%2CcontentPublishTime")

# 解析JSON数据，提取contentId和contentTitle
data=$(echo "$response" | jq --compact-output -r '.data.contentlist[]')

P="https://pay.weixin.qq.com/index.php/public/cms/content_detail?platformType=0&lang=zh&id="
# 初始化最终字符串Z
Z=""
# 当前Unix时间戳
current_timestamp=$(date +%s)
# 昨天的0点0分0秒的时间戳
yesterday_start=$(date -d "yesterday 00:00:00" "+%s")
# 昨天的23点59分59秒的时间戳
yesterday_end=$(date -d "yesterday 23:59:59" "+%s")

# 循环处理每个data对象
for row in $data; do
    contentId=$(echo "$row" | jq --compact-output -r '.contentId')
    contentTitle=$(echo "$row" | jq --compact-output -r '.contentTitle')
    specified_time=$(echo "$row" | jq --compact-output -r '.contentPublishTime')

	# 比较指定变量与昨天的时间戳
	if [ $specified_time -ge $yesterday_start ] && [ $specified_time -le $yesterday_end ]; then
	    # 将字符串Y追加到最终字符串Z
	    echo "News: $row"
        Z="${Z}${contentTitle}: ${P}${contentId} "
	fi
done

if [ "$Z" = '' ]; then
    python send_mail.py WeChat-Pay-Notify "${Z}"
fi
