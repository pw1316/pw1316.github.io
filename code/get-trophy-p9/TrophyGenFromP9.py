#! usr/bin/python
#coding=utf-8
'''
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
'''
import re
import sys
import urllib

def decorate_input_url(strin):
    '''Change gameId to actual URL

    Args:
        strin (str): The gameId we want to fetch

    Returns:
        str: The actual URL of the game in P9
    '''

    assert isinstance(strin, str)
    return 'http://psnine.com/psngame/' + strin

def decorate_output_file(output_file_name, title, table_res):
    '''Change gameId to actual URL

    Args:
        output_file_name (str): The file name to write
        title (str): The title of the HTML doc
        table_res (str): The trophy table

    Returns:
        str: The actual URL of the game in P9
    '''

    assert isinstance(output_file_name, str)
    assert isinstance(title, str)
    assert isinstance(table_res, str)
    output_file = open(output_file_name.decode('UTF-8'), 'wb')
    output_file.write('<!DOCTYPE html>\n')
    output_file.write('<html>\n')
    output_file.write('  <head>\n')
    output_file.write('    <title>' + title + '</title>\n')
    output_file.write('    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n')
    output_file.write('    <meta name="viewport" content="width=device-width">\n')
    output_file.write('    <link rel="stylesheet" href="/stylesheets/p9/p9base.css">\n')
    output_file.write('    <link rel="stylesheet" href="/stylesheets/p9/p9layer.css" ')
    output_file.write('id="layui_layer_p9layercss">\n')
    output_file.write('    <link rel="stylesheet" href="/stylesheets/pw-custom.css">\n')
    output_file.write('    <link rel="Shortcut Icon" href="/src/keyaki.png">\n')
    output_file.write('  </head>\n')
    output_file.write('  <body style="background-color:#4E5566">\n')
    output_file.write('    <div class="box main inner mt40">\n')
    output_file.write(table_res)
    output_file.write('    </div>\n')
    output_file.write('  </body>\n')
    output_file.write('</html>\n')
    output_file.close()

def delete_white_space(doc):
    '''Delete white spaces between tags in a HTML doc

    Args:
        doc (str): The doc to be filtered

    Returns:
        bytes: The doc without white spaces
    '''

    assert isinstance(doc, str)
    return re.sub(r'\r?\n\s*|\t*', r'', doc)

def table_filter(table):
    '''Remove unnecessary infomation in a trophy table

    Args:
        table (str): The HTML table to be filtered

    Returns:
        str: The table with only what we need
    '''

    assert isinstance(table, str)
    match_res = re.search(r'(<table.*?>)(.*?)(</table>)', table)
    assert match_res != None
    table_head = match_res.group(1)
    table = match_res.group(2)
    table_tail = match_res.group(3)
    table_res = '      ' + table_head + '\n'
    table_res = table_res + '      <tr><td><a href="/index.html">Back</a></td></tr>\n'

    match_res = re.search(r'<tr.*?>.*?</tr>', table)
    if match_res:
        tag_tr = match_res.group(0)
        table = table[:match_res.start()] + table[match_res.end():]
        tag_tr = re.sub(r'<img.*?><div.*?>', r'', tag_tr, 1)
        tag_tr = re.sub(r'</div>', r'', tag_tr, 1)
        table_res = table_res + '      ' + tag_tr + '\n'

    while True:
        match_res = re.search(r'<tr.*?>.*?</tr>', table)
        if match_res:
            tag_tr = match_res.group(0)
            table = table[:match_res.start()] + table[match_res.end():]
            # Delete <td> with image
            pattern = r'<td class="t\d" width="\d*?" valign="top" align="center">'
            pattern = pattern + r'<a href=".*?"><img src=".*?" width="\d*?" '
            pattern = pattern + r'height="\d*?" class="imgbg" /></a></td>'
            repl = r''
            tag_tr = re.sub(pattern, repl, tag_tr, 1)
            # Change <em class="h-p r"> to <em class="h-p">
            pattern = r'<em class="h-p r">'
            repl = r'<em class="h-p">'
            tag_tr = re.sub(pattern, repl, tag_tr, 1)
            # Change <a> to <span>
            pattern = r'<a.*?(class[ ]*?=[ ]*?\S+)>(.*?)</a>'
            repl = r'<span \1>\2</span>'
            tag_tr = re.sub(pattern, repl, tag_tr, 1)
            # Delete translation and tips <em>
            pattern = r'<em>.*?</em>'
            repl = r''
            tag_tr = re.sub(pattern, repl, tag_tr, 1)
            pattern = r'<em class="alert-success pd5"><b>\d*?</b> Tips</em>'
            repl = r''
            tag_tr = re.sub(pattern, repl, tag_tr, 1)
            # Delete rare <td>
            pattern = r'<td width="12%" class="twoge t. h-p">.*?</td>'
            repl = r''
            tag_tr = re.sub(pattern, repl, tag_tr, 1)
            table_res = table_res + '      ' + tag_tr + '\n'
        else:
            break

    table_res = table_res + '      ' + table_tail + '\n'
    return table_res

def check_input():
    '''Check input arguments if they are Valid

    Returns:
        list: The filtered argument list
        None: if the arguments are invalid
    '''

    args = sys.argv
    if len(args) < 2:
        print 'usage: %s <game no.> [<type1 type2 ...>]' % args[0]
        print '<game no.>  The game ID in P9'
        print '<type1 ...> Filter game types, default is "PS4"'
        return None
    if len(args) == 2:
        args.append('PS4')
    return args

def main():
    '''Main function

    Returns:
        bool: True if is done, False if error occurs
    '''

    # Arguments
    args = check_input()
    if args is None:
        return False

    # Get Document
    try:
        req = urllib.urlopen(decorate_input_url(args[1]))
        doc = req.read()
        req.close()
    except BaseException:
        print args[1] + "...not found"
        return False
    doc = delete_white_space(doc)

    # Get types block
    match_res = re.search(r'<h1>(.*?)</h1>', doc)
    if match_res:
        type_string = match_res.group(1)
    else:
        type_string = ''
    remote_type_list = []
    # Get each type
    while True:
        match_res = re.search(r'<span.*?>(.*?)</span>', type_string, re.S)
        if match_res:
            remote_type_list.append(match_res.group(1))
            type_string = type_string[:match_res.start()] + type_string[match_res.end():]
        else:
            break
    if remote_type_list == []:
        print args[1] + '...not found'
        return False
    flag = False
    for i in args[2:]:
        if i in remote_type_list:
            flag = True
            break
    if not flag:
        print args[1] + '...not the wanted type'
        return False

    # Process tables
    first_turn = True
    table_res = ''
    while True:
        match_res = re.search(r'<table.*?>.*?</table>', doc)
        if match_res:
            table = match_res.group(0)
            doc = doc[:match_res.start()] + doc[match_res.end():]
            if first_turn:
                first_turn = False
                name = re.search(r'<tr.*?>.*?<p>(.*?)</p>.*?</tr>', table).group(1)
                name = re.sub(r'/|\\|\:|\*|\?|\"|<|>|\|', r'', name)
            table = table_filter(table)
            table_res = table_res + table
        else:
            break

    #write
    output_name = args[1] + '-' + name
    for i in remote_type_list:
        output_name = output_name + '-' + i
    decorate_output_file(output_name + '.html', name, table_res)
    print args[1] + '...done Types: ' + str(remote_type_list) + ' Name: ' + name.decode('UTF-8')
    return True

if __name__ == '__main__':
    main()
