import base64
import os
import json
from markdowngenerator.markdowngenerator import MarkdownGenerator


def genshin_impact_news(doc: MarkdownGenerator):
    activity_txt = 'genshin_impact_activity.txt'
    detail_url_prefix = 'https://ys.mihoyo.com/main/news/detail/'
    if not os.path.isfile(activity_txt):
        return
    # 读取文件中的活动
    news_table = []
    news_len = 10
    content_list = {}
    with open(activity_txt, mode='r', encoding='utf-8') as f:
        i = 0
        for line in f.readlines():
            i = i + 1
            if i > news_len:
                break
            j = json.loads(line)
            content_list[j['contentId']] = line.removesuffix('\n')
            news_table.append({'title': j['title'], 'url': detail_url_prefix + j['contentId']})
    doc.writeTextLine()
    doc.addHeader(level=2, text='Genshin Impact News')
    doc.addTable(header_names=['title', 'url'], dictionary_list=news_table)


def genshin_impact_with(doc: MarkdownGenerator):
    doc.writeTextLine()
    doc.addHeader(level=2, text='Genshin Impact Wishes')
    doc.writeTextLine("[Wish History](./genshin_impact_wish.md)")


def main():
    with MarkdownGenerator(
            # By setting enable_write as False, content of the file is written
            # into buffer at first, instead of writing directly into the file
            # This enables for example the generation of table of contents
            filename="README.md", enable_write=False, syntax='GitHub', enable_TOC=False, linesep='\n'
    ) as doc:
        doc.addHeader(1, "daily-py")
        doc.writeTextLine('每日定时任务')
        genshin_impact_with(doc)
        genshin_impact_news(doc)


if __name__ == "__main__":
    os.system('git config --global user.name ' + os.getenv('GIT_NAME'))
    os.system('git config --global user.email ' + os.getenv('GIT_EMAIL'))
    main()
    os.system('git add README.md')
    os.system('git commit -am \'README.md generate\'')
    os.system('git push')
