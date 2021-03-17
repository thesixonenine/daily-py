import requests
import re
import time
import util


def get_file_from_url() -> str:
    return requests.get("https://copymanga.com/comic/huifushushidechonglairensheng").text


# def write_to_file(html_content: str):
#     f = open("./tempfile/comic.html", mode='w', encoding="utf-8")
#     f.write(html_content)


def is_update(t1: time.struct_time, t2: time.struct_time) -> bool:
    year = t1.tm_year == t2.tm_year
    mon = t1.tm_mon == t2.tm_mon
    mday = t1.tm_mday == t2.tm_mday
    return year and mon and mday


def 回复术士():
    t = get_file_from_url()
    re_compile = re.compile(r">20(.*?)</span>")
    m = re_compile.search(t)
    s = m.group()[1:11]
    uptime = time.strptime(s, "%Y-%m-%d")
    update = util.is_update(uptime)
    if update:
        print("回复术士: 今日已更新")
    else:
        print("回复术士: 今日无更新")


if __name__ == '__main__':
    回复术士()
