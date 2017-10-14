# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import urllib2

pageHeadHint = 79987
pageTailHint = 80000


def docDeleteWhiteSpace(doc):
    doc = re.sub(r'\r?\n\s*|\t*', r'', doc) # Delete \n and SPACES in front of a line and TABS
    doc = re.sub(r'>\s+?<', r'><', doc) # Delete SPACES between tags
    return doc

def getImagesGen(pageNumber = 1):
    host_name = 'http://fl368.com/detail/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/45.0.2454.101 Safari/537.36' # Tend to be a human

    # Pages
    page_index = 1
    page_index_max = 1
    img_num = 0

    while page_index <= page_index_max:
        if page_index != 1:
            urlIn = host_name + str(pageNumber) + '_' + str(page_index) + '.html'
        else:
            urlIn = host_name + str(pageNumber) + '.html'

        # 爬当前页面
        try:
            req = urllib2.Request(urlIn)
            req.add_header('User-Agent', user_agent)
            req = urllib2.urlopen(req)
            doc = req.read()
            req.close()
        except BaseException:
            print 'page %s not found...' % urlIn
            return
        doc = docDeleteWhiteSpace(doc)
        match = re.search(r'<div class="detail">(.*)</div><!--.*?--><div class="pager">(.*?)</div>', doc, re.S)

        main_body = match.group(1)
        page_info = match.group(2)

        page_index_max = len(re.findall(r'<option value=.*?>.*?</option>', page_info, re.S))
        # print 'current max index: %d' % page_index_max

        if page_index == 1:
            description = re.search(r'<h1>(.*?)</h1>', main_body, re.S).group(1).decode('utf-8')
            print '%s | parse? (Y/N)' % description
            res = raw_input()
            if len(res) != 0 and (res[0] == 'N' or res[0] == 'n'):
                return

        # get images from current index
        match = re.findall(r'<img src="(.*?)" .*?>', main_body, re.S)
        for image in match:
            try:
                req = urllib2.Request(image)
                req.add_header('User-Agent', user_agent)
                req = urllib2.urlopen(req)
                img = req.read()
                req.close()
            except BaseException as e:
                print 'image %d:%d not found...' % (pageNumber, page_index)
                return
            if not os.path.exists('.\\' + str(pageNumber)):
                os.mkdir('.\\' + str(pageNumber))
            img_file = open('.\\' + str(pageNumber) + '\\' + str(img_num) + '.jpg', 'wb')
            img_file.write(img)
            img_file.close()
            img_num = img_num + 1

        parse_info = '%s index {0}/{1} | total {2}' % description
        parse_info = parse_info.format(page_index, page_index_max, img_num)
        yield parse_info

        page_index = page_index + 1

    return

def main():
    # First Parameter is the Start Page
    args = sys.argv
    if len(args) < 2:
        start = input('Enter begin number:')
    else:
        start = int(args[1])

    while True:
        for i in getImagesGen(start):
            print i
        start = start + 1
    return True

if __name__ == '__main__':
    main()
