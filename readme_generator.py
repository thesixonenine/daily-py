import os
import json
from markdowngenerator.markdowngenerator import MarkdownGenerator


def genshin_impact_news(doc: MarkdownGenerator):
    genshin_impact_activity_data = 'genshin_impact_activity'
    detail_url_prefix = 'https://ys.mihoyo.com/main/news/detail/'
    if not os.path.isfile(genshin_impact_activity_data):
        return
    # 读取文件中的活动
    news_table = []
    news_len = 10
    content_list = {}
    with open(genshin_impact_activity_data, mode='r', encoding='utf-8') as f:
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


def mys_goods(doc: MarkdownGenerator):
    doc.addHeader(level=2, text='米游社商品')
    f_list = ['hk4e', 'hkrpg', 'bh3', 'nxx', 'bh2', 'bbs']
    goods_data = 'mys_goods.json'
    with open(goods_data, mode='r', encoding='utf-8') as f:
        gd = json.load(f)
        for fm in f_list:
            hk4e_list = gd[fm]
            if not hk4e_list:
                continue
            news_table = []
            for hk4e_item in hk4e_list:
                icon_url = str(hk4e_item['icon'])
                icon_md = '![](' + icon_url + ')'
                icon_new_blank = "<a href = " + icon_url + " target = \"_blank\">商品图片</a>"
                news_table.append({'goods_id': hk4e_item['goods_id'], 'goods_name': hk4e_item['goods_name'],
                                   'next_num': hk4e_item['next_num'],
                                   'account_cycle_limit': hk4e_item['account_cycle_limit'],
                                   'price': hk4e_item['price'], 'icon': icon_new_blank})
            doc.writeTextLine()
            doc.addHeader(level=4, text=fm)
            doc.addTable(header_names=['goods_id', 'goods_name', 'next_num', 'account_cycle_limit', 'price', 'icon'],
                         dictionary_list=news_table)

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
        mys_goods(doc)


if __name__ == "__main__":
    os.system('git config --global user.name ' + os.getenv('GIT_NAME'))
    os.system('git config --global user.email ' + os.getenv('GIT_EMAIL'))
    main()
    os.system('git add README.md')
    os.system('git commit -am \'README.md generate\'')
    os.system('git push')
