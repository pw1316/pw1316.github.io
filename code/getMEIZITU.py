# 爬图工具
# 目标域名：http://www.mzitu.com/
# 迭代爬图
# 限制：
# 必须从每组第一页开始
# 只能从后往前爬

# issues:

pageHeadHint = 79987
pageTailHint = 80000

import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

def docDeleteWhiteSpace(doc):
    assert(isinstance(doc, bytes))
    doc = re.sub(br'\r?\n\s*|\t*', br'', doc) # 删掉换行符和行首空白，删掉制表符
    doc = re.sub(br'>\s+?<', br'><', doc) # 删掉标签之间的空白
    return doc

def getImagesGen(start = 1, end = 0):
    hostName = 'http://www.mzitu.com/'
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36' # 仿人类登录

    # 页码
    pageNumber = start
    pageNumberNext = None
    pageIndex = 1
    pageIndexMax = None

    # 正则匹配式
    pageNumberPartPattern = re.compile(rb'<div class="pagenavi">.*?</div>', re.S) # 组和页码
    pageNumberPattern = re.compile(rb'<a href=(.*?)>.*?</a>', re.S) # 页号
    imgPattern = re.compile(rb'<img src="(.*?)".*?/>', re.S) # 图片地址

    while pageNumber != None:
        if pageIndex != 1:
            urlIn = hostName + str(pageNumber) + '/' + str(pageIndex)
        else:
            urlIn = hostName + str(pageNumber)

        # 爬当前页面
        try:
            req = urllib.request.Request(urlIn)
            req.add_header('User-Agent', userAgent)
            req = urllib.request.urlopen(req)
            doc = req.read()
            req.close()
        except BaseException as e:
            print('page %s not found...' % urlIn)
            return False
        assert isinstance(doc, bytes)
        doc = docDeleteWhiteSpace(doc)

        # 第一页的时候获取下一组的组号和当前组的最大页号
        if pageIndex == 1:
            pageNavi = re.search(pageNumberPartPattern, doc).group(0)
            pageNumberNext = re.search(pageNumberPattern, pageNavi).group(1)[1:-1]
            # 如果有下一页，页号的地址是‘http’开头的，否则是‘/’开头的
            if pageNumberNext[:4] == b'http':
                pageNumberNext = re.sub(hostName.encode(), rb'', pageNumberNext)
                pageNumberNext = int(pageNumberNext)
            else:
                pageNumberNext = None
            pageNavi = re.sub(pageNumberPattern, rb'', pageNavi, 1)
            # 找所有页号里最大的
            pageIndexMax = 0
            while True:
                m = re.search(pageNumberPattern, pageNavi)
                if m == None:
                    break
                max = m.group(1)[1:-1]
                max = re.sub(rb'.*?/', rb'', max, flags = re.S)
                if max == '':
                    max = 1
                else:
                    max = int(max)
                if max > pageIndexMax:
                    pageIndexMax = max
                pageNavi = re.sub(pageNumberPattern, rb'', pageNavi, 1)
        
        # 拿到第一张图的地址并爬下来
        urlIn = re.search(imgPattern, doc).group(1).decode()
        try:
            req = urllib.request.Request(urlIn)
            req.add_header('User-Agent',userAgent)
            req = urllib.request.urlopen(req)
            img = req.read()
            req.close()
        except BaseException as e:
            print('image %d:%d not found...' % (pageNumber, pageIndex))
            return False
        assert isinstance(img, bytes)

        # 创建相应的目录以及图片文件
        if not os.path.exists('.\\' + str(pageNumber)):
            os.mkdir('.\\' + str(pageNumber))
        file = open('.\\' + str(pageNumber) + '\\' + str(pageIndex) + '.jpg', 'wb')
        file.write(img)
        file.close()

        # 一页可能不止一张图，如果有，把剩下的也爬了
        subNumber = 1
        doc = re.sub(imgPattern, rb'', doc, 1)
        while True:
            m = re.search(imgPattern, doc)
            if m == None:
                break
            else:
                subNumber = subNumber + 1
                urlIn = m.group(1).decode()
                try:
                    req = urllib.request.Request(urlIn)
                    req.add_header('User-Agent',userAgent)
                    req = urllib.request.urlopen(req)
                    img = req.read()
                    req.close()
                except BaseException as e:
                    print('image %d:%d:%d not found...' % (pageNumber, pageIndex, subNumber))
                    return False
                file = open('.\\' + str(pageNumber) + '\\' + str(pageIndex) + '(' + str(subNumber) + ').jpg', 'wb')
                file.write(img)
                file.close()
                doc = re.sub(imgPattern, rb'', doc, 1)
        
        # 当前页成功爬完，生成器返回一条信息
        s = 'page {0} {1}/{2}({4}) | next page {3}'
        s = s.format(pageNumber, pageIndex, pageIndexMax, pageNumberNext, subNumber)
        yield s

        # 下一轮迭代
        pageIndex = pageIndex + 1
        if pageIndex > pageIndexMax:
            pageIndex = 1
            pageIndexMax = None
            pageNumber = pageNumberNext
            pageNumberNext = None
        if pageNumber != None and end != 0 and pageNumber > end:
            pageNumber = None

    # 没有下一组了循环结束生成器结束
    print('done...')
    return True

def main():
    # 第一个参数作为起始组号，需手动确保该组存在，若没有参数就提示输入一个数字作为起始组号
    args = sys.argv
    if len(args) < 2:
        start = int(input('Enter begin number(' + str(pageHeadHint) + '):'))
        end = int(input('Enter end number(' + str(pageTailHint) + '):'))
    elif len(args) < 3:
        start = int(args[1])
        end = int(input('Enter end number(' + str(pageTailHint) + '):'))
    else:
        start = int(args[1])
        end = int(args[2])

    # 每次迭代后暂停0.1s
    for i in getImagesGen(start, end):
        print(i)
        time.sleep(0.1)
    return True

if __name__ == '__main__':
    main()
