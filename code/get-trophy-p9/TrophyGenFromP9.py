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


def decorate_input_url(input_url):
    """Change gameId to actual URL

    Args:
        input_url (str): The gameId we want to fetch

    Returns:
        str: The actual URL of the game in P9
    """

    assert isinstance(input_url, str)
    return "http://psnine.com/psngame/" + input_url


def decorate_output_file(output_file_name, title, table_res):
    """Write output html file

    Args:
        output_file_name (str): The file name to write
        title (bytes): The title of the HTML doc
        table_res (bytes): The trophy table

    Returns:
    """

    assert isinstance(output_file_name, str)
    assert isinstance(title, bytes)
    assert isinstance(table_res, bytes)
    output_file = open(output_file_name, "wb")
    output_file.write(b"<!DOCTYPE html>\n")
    output_file.write(b"<html>\n")
    output_file.write(b"  <head>\n")
    output_file.write(b"    <title>" + title + b"</title>\n")
    output_file.write(b"    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">\n")
    output_file.write(b"    <meta name=\"viewport\" content=\"width=device-width\">\n")
    output_file.write(b"    <link rel=\"stylesheet\" href=\"/stylesheets/p9/p9base.css\">\n")
    output_file.write(b"    <link rel=\"stylesheet\" href=\"/stylesheets/p9/p9layer.css\" ")
    output_file.write(b"id=\"layui_layer_p9layercss\">\n")
    output_file.write(b"    <link rel=\"stylesheet\" href=\"/stylesheets/pw-custom.css\">\n")
    output_file.write(b"    <link rel=\"Shortcut Icon\" href=\"/src/keyaki.png\">\n")
    output_file.write(b"  </head>\n")
    output_file.write(b"  <body style=\"background-color:#4E5566\">\n")
    output_file.write(b"    <div class=\"box main inner mt40\">\n")
    output_file.write(table_res)
    output_file.write(b"    </div>\n")
    output_file.write(b"  </body>\n")
    output_file.write(b"</html>\n")
    output_file.close()


def decorate_json_output_file(output_file_name, title, table_res):
    """Write output json file

    Args:
        output_file_name (str): The file name to write
        title (bytes): The title of the HTML doc
        table_res (bytes): The trophy table

    Returns:
    """
    
    assert isinstance(output_file_name, str)
    assert isinstance(title, bytes)
    assert isinstance(table_res, bytes)
    pass

def delete_white_space(doc):
    """Delete white spaces between tags in a HTML doc

    Args:
        doc (bytes): The doc to be filtered

    Returns:
        bytes: The doc without white spaces
    """

    assert isinstance(doc, bytes)
    return re.sub(br"\r?\n\s*|\t*", br"", doc)


def table_filter(table):
    """Remove unnecessary information in a trophy table

    Args:
        table (bytes): The HTML table to be filtered

    Returns:
        bytes: The table with only what we need
    """

    assert isinstance(table, bytes)
    match_res = re.search(br"(<table.*?>)(.*?)(</table>)", table)
    assert match_res is not None
    table_head = match_res.group(1)
    table = match_res.group(2)
    table_tail = match_res.group(3)
    table_res = b"      " + table_head + b"\n"
    table_res = table_res + b"      <tr><td><a href=\"/index.html\">Back</a></td></tr>\n"

    match_res = re.search(br"<tr.*?>.*?</tr>", table)
    if match_res:
        tag_tr = match_res.group(0)
        table = table[:match_res.start()] + table[match_res.end():]
        tag_tr = re.sub(br"<img.*?><div.*?>", br"", tag_tr, 1)
        tag_tr = re.sub(br"</div>", br"", tag_tr, 1)
        table_res = table_res + b"      " + tag_tr + b"\n"

    while True:
        match_res = re.search(br"<tr.*?>.*?</tr>", table)
        if not match_res:
            break
        tag_tr = match_res.group(0)
        table = table[:match_res.start()] + table[match_res.end():]
        # Delete <td> with image
        pattern = br"<td class=\"t\d\" width=\"\d*?\" valign=\"top\" align=\"center\">"
        pattern = pattern + br"<a href=\".*?\"><img src=\".*?\" width=\"\d*?\" "
        pattern = pattern + br"height=\"\d*?\" class=\"imgbg\" /></a></td>"
        repl = b""
        tag_tr = re.sub(pattern, repl, tag_tr, 1)
        # Change <em class="h-p r"> to <em class="h-p">
        pattern = b"<em class=\"h-p r\">"
        repl = b"<em class=\"h-p\">"
        tag_tr = re.sub(pattern, repl, tag_tr, 1)
        # Change <a> to <span>
        pattern = br"<a.*?(class[ ]*?=[ ]*?\S+)>(.*?)</a>"
        repl = br"<span \1>\2</span>"
        tag_tr = re.sub(pattern, repl, tag_tr, 1)
        # Delete translation and tips <em>
        pattern = br"<em>.*?</em>"
        repl = br""
        tag_tr = re.sub(pattern, repl, tag_tr, 1)
        pattern = br"<em class=\"alert-success pd5\"><b>\d*?</b> Tips</em>"
        repl = br""
        tag_tr = re.sub(pattern, repl, tag_tr, 1)
        # Delete rare <td>
        pattern = br"<td width=\"12%\" class=\"twoge t. h-p\">.*?</td>"
        repl = br""
        tag_tr = re.sub(pattern, repl, tag_tr, 1)
        table_res = table_res + b"      " + tag_tr + b"\n"

    table_res = table_res + b"      " + table_tail + b"\n"
    return table_res


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


def main():
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
    except BaseException:
        print(args[1] + "...url open failed")
        return False
    doc = delete_white_space(doc)
    assert isinstance(doc, bytes)

    # Get types block
    match_res = re.search(br"<h1>(.*?)</h1>", doc)
    if match_res:
        type_string = match_res.group(1)
    else:
        type_string = ""
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
    decorate_output_file(output_name + ".html", name, table_res)
    decorate_json_output_file(output_name + ".json", name, table_res)
    print(args[1] + "...done Types: " + str(remote_type_list) + " Name: " + name.decode("UTF-8"))
    return True


if __name__ == "__main__":
    main()
