#! usr/bin/python
# coding=utf-8
import re
import trophy_utils


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
    output_file = open(output_file_name + ".html", "wb")
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


if __name__ == "__main__":
    trophy_utils.parse(table_filter, decorate_output_file)
