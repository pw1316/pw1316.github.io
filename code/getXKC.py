# -*- coding:utf-8 -*-
# py27
import urllib
import urllib2
import re
import sys

# 9478101536096
if len(sys.argv) < 2:
    APPLY_CODE = "9478101536096"
else:
    APPLY_CODE = sys.argv[1]

URL = "http://apply.hzcb.gov.cn/apply/app/status/norm/person"

postdata = {"pageNo":"1", "issueNumber":"201806", "applyCode": APPLY_CODE}
postdata = urllib.urlencode(postdata)

req = urllib2.Request(URL, data=postdata)
res = urllib2.urlopen(req)
result = res.read()
result = re.sub(r"\r?\n\s*|\t*", r"", result)
result = re.sub(r">\s+?<", r"><", result)
match = re.search(r"<table\s+?class=\"ge2_content\".*?><tbody>(.*?)</tbody></table>", result, re.S)
result = (match is not None) and match.group(1) or ""
result = re.sub(r"<tr\s*?.*?>.*?</tr>", r"", result, 1) # ignore title row
rows = re.findall(r"<tr\s*?.*?>.*?</tr>", result)
row = rows[0]
cols = re.findall(r"<td\s*?.*?>(.*?)</td>", row,)
if len(cols) < 2:
    print "Failed"
else:
    print "Succeeded"
# with open("test.html", "w") as f:
#     f.write(result)
