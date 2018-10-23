# Target Host: http://www.mzitu.com/

# issues:
# 57773/40 not exists
# 57773/41 need manual download

pageHeadHint = "1"
pageTailHint = "80000"

import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

def docDeleteWhiteSpace(doc):
    assert(isinstance(doc, bytes))
    doc = re.sub(br"\r?\n\s*|\t*", b"", doc) # CRLF, Line-front, tab
    doc = re.sub(br">\s+?<", br"><", doc) # Between tags
    return doc

def getImagesGen(start = 1, end = 0, pageIndex = 1, pageIndexMax = None):
    hostName = "http://www.mzitu.com/"
    userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36" # Human-like

    # Page number
    pageNumber = start
    pageNumberNext = None

    # Regex
    pageNumberPartPattern = re.compile(br'<div class="pagenavi">.*?</div>', re.S) # Where is page number
    pageNumberPattern = re.compile(br"<a href=(.*?)>.*?</a>", re.S) # Page number
    imgPattern = re.compile(br'<img src="(.*?)".*?/>', re.S) # Image URL

    while pageNumber != None:
        if pageIndex != 1:
            urlIn = hostName + str(pageNumber) + "/" + str(pageIndex)
        else:
            urlIn = hostName + str(pageNumber)

        # Get main page
        try:
            req = urllib.request.Request(urlIn)
            req.add_header("User-Agent", userAgent)
            req = urllib.request.urlopen(req)
            doc = req.read()
            req.close()
        except BaseException as e:
            print("page %s not found..." % urlIn)
            return False
        assert isinstance(doc, bytes)
        doc = docDeleteWhiteSpace(doc)

        # When first page, get next page and max index
        if pageIndex == 1:
            pageNavi = re.search(pageNumberPartPattern, doc).group(0)
            pageNumberNext = re.search(pageNumberPattern, pageNavi).group(1)[1:-1]
            # If there is next, begin with "http", "/" otherwise
            if pageNumberNext[:4] == b"http":
                pageNumberNext = re.sub(hostName.encode(), b"", pageNumberNext)
                pageNumberNext = int(pageNumberNext)
            else:
                pageNumberNext = None
            pageNavi = re.sub(pageNumberPattern, b"", pageNavi, 1)
            # Find max index
            pageIndexMax = 0
            while True:
                m = re.search(pageNumberPattern, pageNavi)
                if m == None:
                    break
                max = m.group(1)[1:-1]
                max = re.sub(br".*?/", b"", max, flags = re.S)
                if max == b"":
                    max = 1
                else:
                    max = int(max)
                if max > pageIndexMax:
                    pageIndexMax = max
                pageNavi = re.sub(pageNumberPattern, b"", pageNavi, 1)
        
        # Get first image's URL
        imageUrlIn = re.search(imgPattern, doc).group(1).decode()
        try:
            req = urllib.request.Request(imageUrlIn)
            req.add_header("User-Agent",userAgent)
            req.add_header("Referer",urlIn)
            req = urllib.request.urlopen(req)
            img = req.read()
            req.close()
        except BaseException as e:
            print("image %d:%d not found..." % (pageNumber, pageIndex))
            return False
        assert isinstance(img, bytes)

        # Create directory and image
        if not os.path.exists("E:\\mzitu\\" + str(pageNumber)):
            os.mkdir("E:\\mzitu\\" + str(pageNumber))
        file = open("E:\\mzitu\\" + str(pageNumber) + "\\" + str(pageIndex) + ".jpg", "wb")
        file.write(img)
        file.close()

        # One page could have multiple images
        subNumber = 1
        doc = re.sub(imgPattern, b"", doc, 1)
        while True:
            m = re.search(imgPattern, doc)
            if m == None:
                break
            else:
                subNumber = subNumber + 1
                imageUrlIn = m.group(1).decode()
                try:
                    req = urllib.request.Request(imageUrlIn)
                    req.add_header("User-Agent",userAgent)
                    req.add_header("Referer",urlIn)
                    req = urllib.request.urlopen(req)
                    img = req.read()
                    req.close()
                except BaseException as e:
                    print("image %d:%d:%d not found..." % (pageNumber, pageIndex, subNumber))
                    return False
                file = open("E:\\mzitu\\" + str(pageNumber) + "\\" + str(pageIndex) + "(" + str(subNumber) + ").jpg", "wb")
                file.write(img)
                file.close()
                doc = re.sub(imgPattern, b"", doc, 1)
        
        # 当前页成功爬完，生成器返回一条信息
        s = "page {0} {1}/{2}({4}) | next page {3}"
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

    # End generator
    print("done...")
    return True

def main():
    args = sys.argv
    if len(args) < 2:
        start = int(input("Enter begin number(" + pageHeadHint + "):") or pageHeadHint)
        end = int(input("Enter end number(" + pageTailHint + "):") or pageTailHint)
        index = int(input("Enter page index(1):") or "1")
        indexMax = input("Enter page max index:")
        indexMax = indexMax and int(indexMax) or None
    elif len(args) < 3:
        start = int(args[1])
        end = int(input("Enter end number(" + pageTailHint + "):") or pageTailHint)
    else:
        start = int(args[1])
        end = int(args[2])
        index = int(input("Enter page index(1):") or "1")
        indexMax = input("Enter page max index:")
        indexMax = indexMax and int(indexMax) or None

    # 0.1s per image, 10s per 10 images
    cnt = 0
    for i in getImagesGen(start, end, index, indexMax):
        print(i)
        cnt += 1
        time.sleep(0.1)
        if cnt % 10 == 0:
            time.sleep(10)
    return True

if __name__ == "__main__":
    main()
