import json
import os
import requests

from send_mail import send_mail_from_txt

detail_url_prefix = 'https://ys.mihoyo.com/main/news/detail/'
activity_txt = 'genshin_impact_activity.txt'
new_content_list = []
content_list = {}


# 文件存在判断
def create_file():
    if not os.path.isfile(activity_txt):
        with open(activity_txt, mode='x') as f:
            pass


def load_file():
    # 读取文件中的活动
    with open(activity_txt, mode='r') as f:
        for line in f.readlines():
            j = json.loads(line)
            content_list[j['contentId']] = line.removesuffix('\n')


# 下载活动
def download_activity(page_num: int, page_size: int):
    try:
        return str(requests.get(
            "https://ys.mihoyo.com/content/ysCn/getContentList?pageSize=" + str(page_size) + "&pageNum=" + str(page_num) + "&channelId=10").content, encoding='utf-8')
    except:
        return ""
    # return str(urlopen("https://ys.mihoyo.com/content/ysCn/getContentList?pageSize=" + str(page_size) + "&pageNum=" + str(page_num) + "&channelId=10").readlines()[0], encoding='utf-8')


# 将新活动加入到file_lines
def deal_data_list(data_list):
    for item in data_list:
        content_id = item['contentId']
        title = item['title']
        detail_url = detail_url_prefix + content_id
        if content_id in content_list:
            continue
        else:
            new_content_list.append(content_id + ' ' + title + ' ' + detail_url)
            content_list[content_id] = json.dumps(item, ensure_ascii=False).removesuffix('\n')


def main():
    create_file()
    load_file()
    # 循环请求所有活动
    page_size = 100
    activity = download_activity(1, 10)
    if "" == activity:
        print("网络异常, 未获取到活动")
        return
    total = json.loads(activity)['data']['total']
    real_true = int(total / page_size)
    if (total / page_size) > real_true:
        real_true = real_true + 1
    for i in range(1, real_true + 1):
        activity = download_activity(i, page_size)
        if "" == activity:
            print("网络异常, 未获取到活动")
            return
        deal_data_list(json.loads(activity)['data']['list'])

    # 将最新的全部活动排序后写入文件
    context = []
    for i in sorted(content_list, key=lambda x: int(x), reverse=True):
        context.append(content_list[i])
    with open(activity_txt, mode='w') as f:
        f.writelines("\n".join(context))

    # 读取文件内容并打印
    # context = ''
    # with open(file="genshin_impact_activity.txt", mode='r') as f:
    #     for line in f.readlines():
    #         context = context + line
    # print(context)
    # f.close()

    # 新活动发送邮件
    if len(new_content_list) > 0:
        mail_content_txt = 'mail_content.txt'
        # 文件存在判断
        with open(mail_content_txt, mode='w') as f:
            f.writelines("\n".join(new_content_list))

        # 发送邮件
        send_mail_from_txt('genshin-impact-news')
        os.system('rm -rf ' + mail_content_txt)
        os.system('git config --global user.name ' + os.getenv('GIT_NAME'))
        os.system('git config --global user.email ' + os.getenv('GIT_EMAIL'))
        os.system('git add genshin_impact_activity.txt')
        os.system('git commit -am \'genshin-impact-news\'')
        os.system('git push')
        print(new_content_list)
    else:
        print('没有新活动')


if __name__ == '__main__':
    main()
