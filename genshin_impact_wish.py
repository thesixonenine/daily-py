import json
import os
import re
import requests

eng_to_zh = dict()


def load_eng_to_zh():
    with open('genshin_impact_eng_to_zh', 'r', encoding='utf-8') as f:
        for line in f:
            (key, val) = line.split('=')
            eng_to_zh[key] = val


def to_zh(s: str):
    return eng_to_zh.get(s, s)


def print_list(l: list):
    s = ""
    for i in range(len(l)):
        s = s + " " + to_zh(l[i])
    return s.removesuffix(" ")


def main():
    load_eng_to_zh()
    with open("manifest.json", "wb") as f:
        f.write(requests.get("https://paimon.moe/manifest.json").content)
    url = None
    file_name = None
    with open('manifest.json', 'r', encoding='utf-8') as f:
        t = f.readlines()
        for idx in range(len(t)):
            match_obj = re.search(r'_app/immutable/chunks/banners-.*js', t[idx], re.M)
            if match_obj is not None:
                url = 'https://paimon.moe/' + match_obj.group()
                # print(url)
                file_name = re.search(r'banners.*js', url, re.M).group()
                # print(file_name)
    os.remove("manifest.json")
    if url is None or file_name is None:
        return

    with open(file_name, "wb") as f:
        f.write(requests.get(url).content)

    with open(file_name, 'r', encoding='utf-8') as f:
        s = f.readlines()[0]
        json_str = re.search(r'{.*?;', s, re.M).group().removesuffix(';')
        # print(json_str)
    if json_str is None:
        return
    os.remove(file_name)
    replace_list = ["beginners:", "name:", "standard:", "characters:", "weapons:",
                    "shortName:", "image:", "start:", "end:", "color:", "timezoneDependent:",
                    "featured:", "featuredRare:", "version:", "timezoneDependentEnd:"]
    for r in replace_list:
        json_str = json_str.replace(r, "\"" + r.removesuffix(":") + "\":")
    json_str = json_str.replace("!0", "\"!0\"")
    j_obj = json.loads(json_str)
    characters = j_obj['characters']
    weapons = j_obj['weapons']
    with open("genshin_impact_wish.md", "w", encoding="UTF-8") as f:
        f.write("## 角色卡池历史\n")
        f.write("| 版本 | 开始时间 | 结束时间 | 五星 | 四星 |\n")
        f.write("| ---- | ---- | ---- | ---- | ---- |\n")
        for i in range(len(characters) - 1, -1, -1):
            wish = characters[i]
            ver = wish['version']
            five_list = wish['featured']
            four_list = wish['featuredRare']
            start = wish['start']
            end = wish['end']
            f.write("| " + ver + " | " + start + " | " + end + " | " + print_list(five_list) + " | " + print_list(four_list) + " |\n")
        f.write("\n\n")
        f.write("## 武器卡池历史\n")
        f.write("| 版本 | 开始时间 | 结束时间 | 五星 | 四星 |\n")
        f.write("| ---- | ---- | ---- | ---- | ---- |\n")
        for i in range(len(weapons) - 1, -1, -1):
            wish = weapons[i]
            ver = wish['version']
            five_list = wish['featured']
            four_list = wish['featuredRare']
            start = wish['start']
            end = wish['end']
            f.write("| " + ver + " | " + start + " | " + end + " | " + print_list(five_list) + " | " + print_list(four_list) + " |\n")


if __name__ == '__main__':
    main()
    os.system('git config --global user.name ' + os.getenv('GIT_NAME'))
    os.system('git config --global user.email ' + os.getenv('GIT_EMAIL'))
    os.system('git add genshin_impact_wish.md')
    os.system('git commit -am \'update genshin impact wish\'')
    os.system('git push')
