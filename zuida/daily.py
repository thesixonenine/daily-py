from bs4 import BeautifulSoup
import requests as rq
import os
import time
import util
curl_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    # 'Origin': 'http://www.zuidazy4.com', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,
    # image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Referer':
    # 'http://www.zuidazy4.com/index.php?m=vod-search', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control':
    # 'max-age=0',

}

url_host = "http://www.zuidazy4.com"


def search_video(video_name):
    url_search = "http://www.zuidazy4.com/index.php?m=vod-search"
    data_para = {
        "wd": video_name,
        "submit": "search",
    }

    resp = rq.post(url=url_search, headers=curl_header, data=data_para)
    soup = BeautifulSoup(resp.content, "lxml")
    card_video = soup.find(name='div', attrs={"class": "xing_vb"})
    list_video = card_video.find_all("ul")[1:-1]
    list_video_info = [parse_video_info(one_video) for one_video in list_video]
    return list_video_info


def parse_video_info(one_video):
    span_name = one_video.find(name="span", attrs={"class": "xing_vb4"})
    href = span_name.find("a").get("href")
    type_name = one_video.find(name="span", attrs={"class": "xing_vb5"})
    update_time = one_video.find(name="span", attrs={"class": "xing_vb6"})
    video_info = {
        "video_name": span_name.text,
        "video_uri": href,
        "video_type": type_name.text,
        "update_time": update_time.text,
    }

    return video_info


def get_video_info(video_uri):
    url = "{}{}".format(url_host, video_uri)
    resp = rq.get(url, headers=curl_header)
    soup = BeautifulSoup(resp.content, "lxml")
    video_header = soup.find(name="div", attrs={"class": "vodh"})
    video_title = video_header.find("h2").text
    video_intros = soup.find(name="div", attrs={"class": "vodinfobox"})
    video_intro_info = parse_video_intro(video_intros)
    video_intro_info["video_name"] = video_title
    m3u8_list = soup.find(name="div", attrs={"id": "play_1"}).find_all("li")
    res_m3u8_list = [m3_info.text.split("$") for m3_info in m3u8_list]

    return video_intro_info, res_m3u8_list


def parse_video_intro(video_intros):
    more_info = video_intros.find(name="span", attrs={"class": "more"}).get("txt")
    list_info = video_intros.find_all("li")
    list_info_text = [li.text for li in list_info]
    director = get_info_value("导演", list_info_text)
    actor = get_info_value("主演", list_info_text)
    time_dur = get_info_value("片长", list_info_text)
    up_time = get_info_value("上映", list_info_text)
    intro_info = {
        "director": director,
        "actor": actor,
        "up_time": up_time,
        "time_dur": time_dur,
        "more_info": more_info
    }

    return intro_info


def get_info_value(val_name, list_info_text):
    for txt in list_info_text:
        if val_name in txt:
            return txt.split("：")[-1].strip()
    return "未知"


def down(ff_path, d_path, f_name):
    print(f_name + " 查询开始")
    video_infos = search_video(f_name)
    o = len(video_infos)
    print('查询到 ' + str(o) + " 个")
    if o != 0:
        pass
        # path_sep = d_path + os.path.sep + f_name
        # os.makedirs(name=path_sep)
    for video_info in video_infos:
        print()
        print()
        print(video_info)
        print()
        intro, m3_list = get_video_info(video_info["video_uri"])
        # print(intro)
        for m in m3_list:
            # print(m)
            print(('{} -i {} -c copy {}' + os.path.sep + '{}.mp4').format(ff_path, m[1], d_path, m[0]))


def search_download():
    ffmpeg_path = 'D:\\ffmpeg-4.2.3-win64-static\\bin\\ffmpeg.exe'
    download_path = "D:\\ffmpeg-4.2.3-win64-static\\down"
    # 缘之空
    video_name = "缘之空"
    down(ffmpeg_path, download_path, video_name.strip().replace(' ', '_'))

def 缘之空():
    video_infos = search_video("缘之空")
    intro, m3_list = get_video_info(video_infos[0]["video_uri"])
    uptime = time.strptime("", "%Y-%m-%d")
    update = util.is_update(uptime)
    if update:
        print("回复术士: 今日已更新")
    else:
        print("回复术士: 今日无更新")
if __name__ == '__main__':
    # search_download()
    缘之空()

    pass
