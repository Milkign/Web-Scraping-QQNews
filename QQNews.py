from bs4 import BeautifulSoup
import requests


# 解析网页
def getHTMLText(path):
    try:
        # 网络超时30秒
        r = requests.get(path, 'html.parser', timeout=30)
        #  引发HTTPError异常
        r.raise_for_status()
        #  用网页实际字符集替代默认字符集
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print(e)


# 获取新闻列表
def getQQNewsItems(text, itemList):
    # 创建BeautifulSoup对象，html.parser是python自带的网页解析库
    soup = BeautifulSoup(text, 'html.parser')
    # 获取指定的标签的内容，并生成列表  item则为每一条数据的内容
    for item in soup.select(
            'div.Q-tpList div div.text em a,div.Q-pList div.content em a'):
        # 其中数据封装成列表 append：末尾增加参数
        itemList.append([item["href"], item.string])


# 获取新闻文章内容
def getNewsText(url):
    # 防止获取到的链接格式出错，进行手动格式化，如果没有http:就加上
    if not url.startswith('http:'):
        # 格式化链接
        url = 'http:' + url
        # 解析新闻链接
        text = getHTMLText(url)
        # 创建BeautifulSoup对象
        soup1 = BeautifulSoup(text, 'html.parser')

        # 获取新闻文章内容并存储到列表

        # 创建新闻文章列表
        article = []
        # 获取新闻文章内容
        for item in soup1.select('div.content-article p.one-p'):
            # 文字、图片、视频item.string的值是none，只将文字存入article新闻文章列表
            if item.string != None:
                article.append(item.string)
        # 去空格
        article = [item.replace('\u3000', '') for item in article]
        # 合并列表
        article = ''.join(article)
        # 将获取的新闻文章列表返回
        return article


# 数据存储
def getNewsContent(itemList):
    # itemList是获取的新闻列表，item[0]是新闻链接，item[1]是新闻标题
    for item in itemList:
        # 从每条新闻的链接中获取对应新闻文章内容
        content = getNewsText(item[0])

        #  使用文件 存入文件内
        f = open("text.txt", "a", encoding='utf-8')
        # 存储新闻标题
        # 判断内容是否为空，不为空则写入txt文件
        if item[1] != None:
            f.write(item[1] + "\n")
        # 存储新闻链接
        if item[0] != None:
            f.write(item[0] + "\n")
        # 存储新闻内容
        if content != None:
            f.write(content + "\n")
        # 关闭文件
        f.close()

# 爬取的目标网址
url = 'http://society.qq.com/'
# 解析网址
text = getHTMLText(url)
#创建列表，用于存储新闻信息
itemList = []
# 获取新闻列表，并存储在itemList中
getQQNewsItems(text, itemList)
# 根据itemList中存储的新闻链接，爬取新闻文章内容，并存储到txt文件中
getNewsContent(itemList)
