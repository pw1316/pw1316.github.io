# coding=utf-8
"""Utils for both to html and to json."""
import argparse
import re
import urllib.request
import urllib.error

from logger import LOGGER as logger


def dump_doc(doc):
    """Dump doc to a file and exit."""
    assert isinstance(doc, bytes)
    with open("dump.html", "wb") as ifs:
        ifs.write(doc)
    logger.error("dump done.")


def _game_no_2_url(game_no):
    assert isinstance(game_no, int)
    return "https://psnine.com/psngame/%d" % game_no


def _delete_white_space(doc):
    assert isinstance(doc, bytes)
    doc = re.sub(br"\r?\n\s*|\t*", b"", doc)
    doc = re.sub(br">\s+?<", br"><", doc)
    return doc


def _check_input():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "game_no",
        type=int,
        help="The game ID in P9",
        metavar="<game no.>"
    )
    parser.add_argument(
        "-t",
        nargs="*",
        default=["PS4"],
        type=str,
        help="Filter game types, default is \"PS4\"",
        metavar="<type>",
        dest="type"
    )
    flxg = parser.parse_args()
    return flxg


def _game_no_2_doc(game_no):
    assert isinstance(game_no, int)
    input_url = _game_no_2_url(game_no)
    try:
        req = urllib.request.urlopen(input_url)
        doc = req.read()
        req.close()
    except urllib.error.URLError:
        logger.error("[%d] url open failed", game_no)
    doc = _delete_white_space(doc)
    return doc


def _game_type_check(game_no, type_need, doc):
    assert isinstance(game_no, int)
    assert isinstance(type_need, list)
    assert isinstance(doc, bytes)
    # All type info in a <h1> tag
    match_res = re.search(br"<h1>(.*?)</h1>", doc)
    doc = match_res.group(1) if match_res else b""

    # Each type in a <span> tag with attributes
    type_list = []
    match_res = re.search(br"<span.*?>(.*?)</span>", doc, re.S)
    while match_res:
        type_list.append(match_res.group(1).decode("utf-8"))
        doc = doc[:match_res.start()] + doc[match_res.end():]
        match_res = re.search(br"<span.*?>(.*?)</span>", doc, re.S)

    for i in type_need:
        if i in type_list:
            logger.info("[%d] %s matches %s", game_no, i, type_list)
            return type_list
    logger.error("[%d] %s not match %s", game_no, type_need, type_list)


def parse(table_filter, output_writer):
    """
    Parse trophy main function.

    Returns:
        bool: True if is done, False if error occurs
    """
    args = _check_input()
    doc = _game_no_2_doc(args.game_no)
    _game_type_check(args.game_no, args.type, doc)

    # Process tables
    first_turn = True
    name = b""
    table_res = b""
    match_res = re.search(br"<table.*?>.*?</table>", doc)
    while match_res:
        table = match_res.group(0)
        doc = doc[:match_res.start()] + doc[match_res.end():]
        # Get game name in first turn
        if first_turn:
            first_turn = False
            name = re.search(
                br"<tr.*?>.*?<p>(.*?)</p>.*?</tr>", table
            ).group(1)
            name = re.sub(br"[/\\:*?\"<>|]", br"", name)
        table = table_filter(table)
        table_res = table_res + table
        match_res = re.search(br"<table.*?>.*?</table>", doc)

    # write
    output_name = "%d-%s" % (args.game_no, name.decode("utf-8"))
    output_writer(output_name, name, table_res)
    logger.info("[%d] name: %s", args.game_no, name.decode("utf-8"))
    return True
