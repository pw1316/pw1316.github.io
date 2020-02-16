# coding=utf-8
"""Save to json."""
import re

import trophy_utils


def decorate_output_file(output_file_name, title, table_res):
    """
    Write output json file.

    Args:
        output_file_name (str): The file name to write
        title (bytes): The title of the json doc
        table_res (bytes): The trophy table
    """
    assert isinstance(output_file_name, str)
    assert isinstance(title, bytes)
    assert isinstance(table_res, bytes)
    table_res = table_res[:-1] if table_res else table_res
    with open(output_file_name + ".json", "wb") as ofs:
        ofs.write(b'{"name":"%s","trophy":[%s]}' % (title, table_res))


def table_filter(doc_table):
    """
    Remove unnecessary information in a trophy table.

    Args:
        doc_table (bytes): The HTML table to be filtered

    Returns:
        bytes: The table with only what we need
    """
    assert isinstance(doc_table, bytes)
    res = b""

    doc_table = re.search(br"<table.*?>(.*?)</table>", doc_table).group(1)
    doc_table = re.sub(br"<tr.*?>.*?</tr>", b"", doc_table, 1)

    match = re.search(br'<tr id="(.*?)">(.*?)</tr>', doc_table)
    while match:
        doc_table = doc_table[:match.start()] + doc_table[match.end():]
        trophy_id = int(match.group(1))
        doc_tr = match.group(2)

        # Delete first tag <td>
        doc_tr = re.sub(br"<td.*?>.*?</td>", b"", doc_tr, 1)

        # type & name are in tag <a>
        match = re.search(
            br'<a.*?class[ ]*?=[ ]*?"(.+?)">(.*?)</a>', doc_tr, re.S
        )
        trophy_type = match.group(1)
        trophy_name = match.group(2).replace(b"\"", b"'")

        doc_tr = doc_tr[:match.start()] + doc_tr[match.end():]
        doc_tr = re.sub(br"<p>.*?</p>", b"", doc_tr, 1)

        # desc is in remaining tag <em>
        trophy_desc = re.search(
            br'<em class="text-gray">(.*?)</em>',
            doc_tr, re.S
        ).group(1).replace(b"\"", b"'")

        res += b'{"id":%d,"type":"%s","name":"%s","desc":"%s","done":0},'\
            % (trophy_id, trophy_type, trophy_name, trophy_desc)
        match = re.search(br'<tr id="(.*?)">(.*?)</tr>', doc_table)
    return res


if __name__ == "__main__":
    trophy_utils.parse(table_filter, decorate_output_file)
