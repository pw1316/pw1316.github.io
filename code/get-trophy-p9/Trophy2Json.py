#! usr/bin/python
# coding=utf-8
import re
import TrophyUtils


def decorate_output_file(output_file_name, title, table_res):
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
    output_file = open(output_file_name + ".json", "wb")
    output_file.write(b'{"name":"%s","trophy":[%s]}' % (title, table_res and table_res[:-1] or table_res))
    output_file.close()


def table_filter(table):
    """Remove unnecessary information in a trophy table

    Args:
        table (bytes): The HTML table to be filtered

    Returns:
        bytes: The table with only what we need
    """

    assert isinstance(table, bytes)
    table = re.search(br"<table.*?>(.*?)</table>", table).group(1)
    table = re.sub(br"<tr.*?>.*?</tr>", b"", table, 1)
    table_res = b""

    while True:
        match_res = re.search(br'<tr id="(.*?)">(.*?)</tr>', table)
        if not match_res:
            break
        table = table[:match_res.start()] + table[match_res.end():]
        trophy_id = int(match_res.group(1))
        trophy_tr = match_res.group(2)

        # Delete <td> with image
        trophy_tr = re.sub(br"<td.*?>.*?</td>", b"", trophy_tr, 1)

        match_res = re.search(br'<a.*?class[ ]*?=[ ]*?"(.+?)">(.*?)</a>', trophy_tr, re.S)
        trophy_type = match_res.group(1)
        trophy_name = match_res.group(2).replace(b"\"", b"'")

        trophy_tr = trophy_tr[:match_res.start()] + trophy_tr[match_res.end():]
        trophy_tr = re.sub(br"<p>.*?</p>", b"", trophy_tr, 1)

        trophy_desc = re.search(br'<em class="text-gray">(.*?)</em>', trophy_tr, re.S).group(1).replace(b"\"", b"'")

        table_res += b'{"id":%d,"type":"%s","name":"%s","desc":"%s"},'\
                     % (trophy_id, trophy_type, trophy_name, trophy_desc)

    return table_res


if __name__ == "__main__":
    TrophyUtils.parse(table_filter, decorate_output_file)
