# 导入模块
import requests
from lxml import etree
import csv

# 请求头
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}

# 数据列表
lst = []

# 翻页
for page in range(1, 11):
    # 目标 url
    url = f'https://movie.douban.com/top250?start={(page-1) * 25}&filter='

    # 发请求，获取响应
    res = requests.get(url, headers=head)

    # 创建对象
    html = etree.HTML(res.text)

    # 数据解析
    divs = html.xpath('//div[@class="info"]')

    # 循环遍历拿到每一组数据
    for div in divs:  # 每一组数据的获取
        # 创建对象
        dic = {}
        # 标题
        title = div.xpath('./div[@class="hd"]/a//text()')
        dic['titls'] = ''.join(title).replace(' ', '').replace('\n', '')
        # 电影类型
        dic['types'] = div.xpath('./div[@class="bd"]/p/text()')[1].split('/')[-1].strip()
        # 电影评分
        dic['star'] = div.xpath('./div[@class="bd"]/div[@class="star"]/span[2]/text()')[0]
        # 引言，没有获取到数据，返回是一个空列表
        quote = div.xpath('./div[@class="bd"]/p[@class="quote"]/span/text()')
        # 判断是否为空列表
        if quote: # 如果不是就直接取下标值
            dic['quote'] = quote[0]
        else: # 如果是的，就赋值为空字符串
            dic['quote'] = ''
        # 在列表数据中增加对象数据
        lst.append(dic)

# 设置表头，与对象中的 key 值相同
head = ('titls', 'types', 'star', 'quote')

# 创建文件对象
with open('douban.csv','w',encoding='utf-8-sig',newline='') as f:
    # 创建 csv 写入对象
    writer = csv.DictWriter(f, fieldnames=head)
    # 写入表头
    writer.writeheader()
    # 写入数据
    writer.writerows(lst)