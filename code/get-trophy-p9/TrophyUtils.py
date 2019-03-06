#! usr/bin/python
# coding=utf-8
"""
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
#   <em>TROPHY TRANSLATION</em><em class="alert-success pd5"><b>TIP NUM</b> Tips</em></p>
#   <em class="text-gray">TROPHY DESCRIPTION</em>
#   <div class="text-strong mt10">TROPHY DESCRIPTION TRANSLATION</div>
#   </td>
#   <td width="12%" class="twoge t? h-p">???<em>珍贵度</em></td>
#   </tr>
# </table>
"""
import re
import sys
import urllib.request
import urllib.error


def dump_doc(doc):
    assert isinstance(doc, bytes)
    with open("dump.html", "wb") as f:
        f.write(doc)
    exit(1)
    pass


def decorate_input_url(input_url):
    """Change gameId to actual URL

    Args:
        input_url (str): The gameId we want to fetch

    Returns:
        str: The actual URL of the game in P9
    """

    assert isinstance(input_url, str)
    return "https://psnine.com/psngame/" + input_url


def delete_white_space(doc):
    """Delete white spaces between tags in a HTML doc

    Args:
        doc (bytes): The doc to be filtered

    Returns:
        bytes: The doc without white spaces
    """

    assert isinstance(doc, bytes)
    doc = re.sub(br"\r?\n\s*|\t*", b"", doc)
    doc = re.sub(br">\s+?<", br"><", doc)
    return doc


def check_input():
    """Check input arguments if they are Valid

    Returns:
        list: The filtered argument list
        None: if the arguments are invalid
    """

    args = sys.argv
    if len(args) < 2:
        print("usage: %s <game no.> [<type1 type2 ...>]" % args[0])
        print("<game no.>  The game ID in P9")
        print("<type1 ...> Filter game types, default is \"PS4\"")
        return None
    if len(args) == 2:
        args.append("PS4")
    return args


def parse(table_filter, output_writer):
    """Main function

    Returns:
        bool: True if is done, False if error occurs
    """

    # Arguments
    args = check_input()
    if args is None:
        return False

    # Get Document
    try:
        req = urllib.request.urlopen(decorate_input_url(args[1]))
        doc = req.read()
        req.close()
    except urllib.error.URLError:
        print(args[1] + "...url open failed")
        return False
    doc = delete_white_space(doc)
    assert isinstance(doc, bytes)

    # Get types block
    match_res = re.search(br"<h1>(.*?)</h1>", doc)
    if match_res:
        type_string = match_res.group(1)
    else:
        type_string = b""
    remote_type_list = []
    # Get each type
    while True:
        match_res = re.search(br"<span.*?>(.*?)</span>", type_string, re.S)
        if match_res:
            remote_type_list.append(match_res.group(1))
            type_string = type_string[:match_res.start()] + type_string[match_res.end():]
        else:
            break
    if not remote_type_list:
        print(args[1] + "...no remote types")
        return False
    flag = False
    for i in args[2:]:
        if i.encode("utf-8") in remote_type_list:
            flag = True
            break
    if not flag:
        print(args[1] + "...no type matches")
        return False

    # Process tables
    first_turn = True
    name = b""
    table_res = b""
    while True:
        match_res = re.search(br"<table.*?>.*?</table>", doc)
        if not match_res:
            break
        table = match_res.group(0)
        doc = doc[:match_res.start()] + doc[match_res.end():]
        # Get game name in first turn
        if first_turn:
            first_turn = False
            name = re.search(br"<tr.*?>.*?<p>(.*?)</p>.*?</tr>", table).group(1)
            name = re.sub(br"[/\\:*?\"<>|]", br"", name)
        table = table_filter(table)
        table_res = table_res + table

    # write
    output_name = args[1] + "-" + name.decode("UTF-8")
    for i in remote_type_list:
        output_name = output_name + "-" + i.decode("UTF-8")
    output_writer("Trophies", name, table_res)
    print(args[1] + "...done Types: " + str(remote_type_list) + " Name: " + name.decode("UTF-8"))
    return True
