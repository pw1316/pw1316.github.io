---
layout: trophy
title: "Dark Souls 3 wiki"
image: http://wx1.sinaimg.cn/thumb150/bfae17b6ly1ffyzgsk4czj20sg0sgx6p
alt: "Dark Souls 3 wiki"
---

<tr><td colspan="4"><p>{{ site.data.DS3.Trophies.name }}</p></td></tr>

{% for item in site.data.DS3.Trophies.trophy %}
{% include trophy_item.html %}
{% endfor %}
