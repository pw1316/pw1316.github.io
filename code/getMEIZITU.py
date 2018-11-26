# Target Host: http://www.mzitu.com/

# Updates:
# 2018-11-23 Protocol http->https, and some sites are gzipped
# 2018-10-23 Add http referer

# issues:
# 57773/40 not exists
# 57773/41 need manual download
# 150343/41 not exists

import gzip
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

pageHeadHint = '1'
pageTailHint = '200000'


def doc_delete_white_space(doc):
    """Delete the white space
    Args:
      doc(bytes): Document to be processed.
    Returns:
      Document without white spaces.
    """
    assert(isinstance(doc, bytes))
    doc = re.sub(br'\r?\n\s*|\t*', b'', doc)  # CRLF, Line-front, tab
    doc = re.sub(br'>\s+?<', br'><', doc)  # Between tags
    return doc


def get_image_gen(start=1, end=0, page_index=1, page_index_max=None):
    """Delete the white space.
    Args:
        start(int): Start page number.
        end(int): Upper bound of end page number
        page_index(int): Index of the first page
        page_index_max(int): If "page_index" is not 1, should specify the max index of the first page, otherwise None
    Returns:
        A generator
    """
    host_name = 'https://www.mzitu.com/'
    # Like human
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/45.0.2454.101 ' \
                 'Safari/537.36 '

    # Page number
    page_number = start
    page_number_next = None

    # Regex
    page_number_part_pattern = re.compile(br'<div class="pagenavi">.*?</div>', re.S)  # Where is page number
    page_number_pattern = re.compile(br'<a href=(.*?)>.*?</a>', re.S)  # Page number
    img_pattern = re.compile(br'<img src="(.*?)".*?/>', re.S)  # Image URL

    while page_number is not None:
        if page_index != 1:
            url_in = '{}{:d}/{:d}'.format(host_name, page_number, page_index)
        else:
            url_in = '{}{:d}'.format(host_name, page_number)

        # Get main page
        try:
            req = urllib.request.Request(url_in)
            req.add_header('User-Agent', user_agent)
            req = urllib.request.urlopen(req)
            doc = req.read()
            # Gzip
            if req.getheader('Content-Encoding') == 'gzip':
                doc = gzip.decompress(doc)
            req.close()
        except BaseException as e:
            print(e, 'page {} not found...'.format(url_in))
            return False
        assert isinstance(doc, bytes)
        doc = doc_delete_white_space(doc)

        # When first page, get next page and max index
        if page_index == 1:
            page_navi = re.search(page_number_part_pattern, doc).group(0)
            page_number_next = re.search(page_number_pattern, page_navi).group(1)[1:-1]
            # If there is next, begin with "http", "/" otherwise
            if page_number_next[:4] == b'http':
                page_number_next = re.sub(host_name.encode(), b'', page_number_next)
                page_number_next = int(page_number_next)
            else:
                page_number_next = None
            page_navi = re.sub(page_number_pattern, b'', page_navi, 1)
            # Find max index
            page_index_max = 0
            while True:
                m = re.search(page_number_pattern, page_navi)
                if m is None:
                    break
                max_pattern = m.group(1)[1:-1]
                max_pattern = re.sub(br'.*?/', b'', max_pattern, flags=re.S)
                if max_pattern == b'':
                    max_pattern = 1
                else:
                    max_pattern = int(max_pattern)
                if max_pattern > page_index_max:
                    page_index_max = max_pattern
                page_navi = re.sub(page_number_pattern, b'', page_navi, 1)
        
        # Get first image's URL
        image_url_in = re.search(img_pattern, doc).group(1).decode()
        try:
            req = urllib.request.Request(image_url_in)
            req.add_header('User-Agent', user_agent)
            req.add_header('Referer', url_in)  # Need referer
            req = urllib.request.urlopen(req)
            img = req.read()
            req.close()
        except BaseException as e:
            print('image {:d}:{:d} not found...'.format(page_number, page_index))
            print(e)
            return False
        assert isinstance(img, bytes)

        # Create directory and image
        if not os.path.exists('E:\\mzitu\\{:d}'.format(page_number)):
            os.mkdir('E:\\mzitu\\{:d}'.format(page_number))
        file = open('E:\\mzitu\\{:d}\\{:d}.jpg'.format(page_number, page_index), 'wb')
        file.write(img)
        file.close()

        # One page could have multiple images
        sub_number = 1
        doc = re.sub(img_pattern, b'', doc, 1)
        while True:
            m = re.search(img_pattern, doc)
            if m is None:
                break
            else:
                sub_number = sub_number + 1
                image_url_in = m.group(1).decode()
                try:
                    req = urllib.request.Request(image_url_in)
                    req.add_header('User-Agent', user_agent)
                    req.add_header('Referer', url_in)  # Need referer
                    req = urllib.request.urlopen(req)
                    img = req.read()
                    req.close()
                except BaseException as e:
                    print('image {:d}:{:d}:{:d} not found...'.format(page_number, page_index, sub_number))
                    print(e)
                    return False
                file = open('E:\\mzitu\\{:d}\\{:d}({:d}).jpg'.format(page_number, page_index, sub_number), 'wb')
                file.write(img)
                file.close()
                doc = re.sub(img_pattern, b'', doc, 1)
        
        # Yield a message when one iteration done
        s = 'page {0} {1}/{2}({4}) | next page {3}'
        s = s.format(page_number, page_index, page_index_max, page_number_next, sub_number)
        yield s

        # Next iteration
        page_index = page_index + 1
        if page_index > page_index_max:
            page_index = 1
            page_index_max = None
            page_number = page_number_next
            page_number_next = None
        if page_number is not None and end != 0 and page_number > end:
            page_number = None

    # End generator
    print('done...')
    return True


def main():
    args = sys.argv
    argc = len(args)
    start = argc < 2 and int(input('Enter begin number({}):'.format(pageHeadHint)) or pageHeadHint) or int(args[1])
    end = argc < 3 and int(input('Enter end number({}):'.format(pageTailHint)) or pageTailHint) or int(args[2])
    index = int(input('Enter page index(1):') or '1')
    index_max = input('Enter page max index:')
    index_max = index_max and int(index_max) or None

    # 0.1s per image, 10s per 10 images
    cnt = 0
    for i in get_image_gen(start, end, index, index_max):
        print(i)
        cnt += 1
        time.sleep(0.1)
        if cnt % 10 == 0:
            time.sleep(10)
    return True


if __name__ == '__main__':
    main()
