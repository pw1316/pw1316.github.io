"""
Target Host: http://www.mzitu.com/ .

Updates:
2018-11-23 Protocol http->https, and some sites are gzipped
2018-10-23 Add http referer

Issues:
"""
import argparse
import gzip
import os
import re
import time
import urllib.request
import urllib.parse
import urllib.error

HOST_NAME = 'https://www.mzitu.com/'

# Like human
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
    'Chrome/45.0.2454.101 ' \
    'Safari/537.36 '


def doc_delete_white_space(doc):
    """
    Delete the white space.

    Args:
        doc(bytes): Document to be processed.
    Returns:
        Document without white spaces.

    """
    assert isinstance(doc, bytes)
    doc = re.sub(br'\r?\n\s*|\t*', b'', doc)  # CRLF, Line-front, tab
    doc = re.sub(br'>\s+?<', br'><', doc)  # Between tags
    return doc


def get_max_index_and_next(doc):
    """
    Find the max index of current page, and next page.

    Args:
        doc(bytes): Document to be processed.
    Returns:
        Max index of this page.
        Number of next page.

    """
    assert isinstance(doc, bytes)
    pattern_pagenavi = re.compile(br'<div class="pagenavi">.*?</div>', re.S)
    pattern_pagenum = re.compile(br'<a href=(.*?)>.*?</a>', re.S)
    page_navi = pattern_pagenavi.search(doc).group(0)

    num_next = pattern_pagenum.search(page_navi).group(1)[1:-1]
    # If there is next, begin with "http", "/" otherwise
    if num_next[:4] == b'http':
        num_next = re.sub(HOST_NAME.encode(), b'', num_next)
        num_next = int(num_next)
    else:
        num_next = None
    page_navi = pattern_pagenum.sub(b'', page_navi, 1)

    # Find max index
    idx_max = 0
    match = pattern_pagenum.search(page_navi)
    while match:
        idx = match.group(1)[1:-1]
        idx = re.sub(br'.*?/', b'', idx, flags=re.S)
        if idx == b'':
            idx = 1
        else:
            idx = int(idx)
        if idx > idx_max:
            idx_max = idx
        page_navi = pattern_pagenum.sub(b'', page_navi, 1)
        match = pattern_pagenum.search(page_navi)
    return idx_max, num_next


def http_get_main_page(url_in):
    """
    Request page through URL.

    Args:
        url_in(str): Requested URL.
    Returns:
        Page bytes.

    """
    try:
        req = urllib.request.Request(url_in)
        req.add_header('User-Agent', USER_AGENT)
        req = urllib.request.urlopen(req)
        doc = req.read()
        # GZip
        if req.getheader('Content-Encoding') == 'gzip':
            doc = gzip.decompress(doc)
        doc = doc_delete_white_space(doc)
        req.close()
    except urllib.error.HTTPError as error:
        doc = None
        print('[{}] page {} not found...'.format(error.code, url_in))
    return doc


def http_get_image(url_in):
    """
    Request image through URL.

    Args:
        url_in(str): Requested URL.
    Returns:
        Image bytes.

    """
    try:
        req = urllib.request.Request(url_in)
        req.add_header('User-Agent', USER_AGENT)
        req.add_header('Referer', url_in)  # Need referer
        req = urllib.request.urlopen(req)
        image = req.read()
        req.close()
    except urllib.error.HTTPError as error:
        image = None
        print('[{}] image request {} failed...'.format(error.code, url_in))
    return image


def get_image_gen(start, out_dir):
    """
    MZITU image generator.

    Args:
        start(int): Start page number.
        out_dir(str): Output Directory.
    Returns:
        A generator

    """
    # Page number
    num_current = start
    num_next = None
    idx_current = 1
    idx_max = None

    # Regex
    img_pattern = re.compile(br'<img src="(.*?)".*?/>', re.S)  # Image URL

    while num_current is not None:
        if idx_current != 1:
            url_in = '{}{:d}/{:d}'.format(HOST_NAME, num_current, idx_current)
        else:
            url_in = '{}{:d}'.format(HOST_NAME, num_current)

        # Get main page
        doc = http_get_main_page(url_in)
        if doc is None:
            return False

        # When first page, get next page and max index
        if idx_current == 1:
            idx_max, num_next = get_max_index_and_next(doc)

        # Get first image's URL
        image_url_in = img_pattern.search(doc).group(1).decode()
        image = http_get_image(image_url_in)
        if image is None:
            return False

        # Create directory and image
        image_dir = os.path.join(out_dir, '{:d}'.format(num_current))
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, '{:d}.jpg'.format(idx_current))
        with open(image_path, 'wb') as ofs:
            ofs.write(image)

        # One page could have multiple images
        sub_number = 1
        doc = img_pattern.sub(b'', doc, 1)
        match = img_pattern.search(doc)
        while match:
            sub_number = sub_number + 1
            image_url_in = match.group(1).decode()
            image = http_get_image(image_url_in)
            if image is None:
                return False
            image_path = os.path.join(
                image_dir, '{:d}({:d}).jpg'.format(idx_current, sub_number))
            with open(image_path, 'wb') as ofs:
                ofs.write(image)
            doc = img_pattern.sub(b'', doc, 1)
            match = img_pattern.search(doc)

        # Yield a message when one iteration done
        yield 'page {0} {1}/{2}({4}) | next page {3}'.format(
            num_current, idx_current, idx_max, num_next, sub_number)

        # Next iteration
        idx_current = idx_current + 1
        if idx_current > idx_max:
            idx_current = 1
            idx_max = None
            num_current = num_next
            num_next = None

    # End generator
    print('done...')
    return True


def _call(start, out_dir):
    # 0.1s per image, 10s per 10 images
    cnt = 0
    for i in get_image_gen(start, out_dir):
        print(i)
        cnt += 1
        time.sleep(0.1)
        if cnt % 10 == 0:
            time.sleep(10)
    return True


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-start', type=int,
        required=True,
        help='Start Number'
    )
    parser.add_argument(
        '-out', type=str,
        required=True,
        help='Output Directory'
    )
    return parser.parse_args()


if __name__ == '__main__':
    FLXG = _parse_arguments()
    _call(FLXG.start, FLXG.out)
