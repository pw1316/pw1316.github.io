# coding=utf-8
"""
Main Structure.

# <table cellpadding="12" cellspacing="0" border="0" width="100%" class="list">
#   <tr><td colspan="4">
#     <img src="???" width="100" height="55" class="imgbgnb l">
#     <div class="ml110">
#     <p>???</p>
#     <em>
#     <span class="text-platinum">???</span>
#     <span class="text-gold">???</span>
#     <span class="text-silver">???</span>
#     <span class="text-bronze">???</span>
#     <span class="text-strong">???</span>
#     </em>
#     </div>
#   </td></tr>
#   <tr id="ID">
#   <td class="t???" width="54" valign="top" align="center">
#     <a href="???"><img src="???" width="54" height="54" class="imgbg" /></a>
#   </td>
#   <td>
#   <p>
#   <em class="h-p r">#???</em>
#   <a href="???" class="text-platinum">TROPHY NAME</a>
#   <em>TROPHY TRANSLATION</em>
#   <em class="alert-success pd5"><b>TIP NUM</b> Tips</em>
#   </p>
#   <em class="text-gray">TROPHY DESCRIPTION</em>
#   <div class="text-strong mt10">TROPHY DESCRIPTION TRANSLATION</div>
#   </td>
#   <td width="12%" class="twoge t? h-p">???<em>珍贵度</em></td>
#   </tr>
# </table>
"""
import argparse
import re
import urllib.request
import urllib.error

from logger import LOGGER as logger


def _dump_doc(doc):
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
            name = re.sub(br"[ ]", br"_", name)
        table = table_filter(table)
        table_res = table_res + table
        match_res = re.search(br"<table.*?>.*?</table>", doc)

    # write
    output_name = "%d-%s" % (args.game_no, name.decode("utf-8"))
    output_writer(output_name, name, table_res)
    logger.info("[%d] name: %s", args.game_no, name.decode("utf-8"))
    return True
