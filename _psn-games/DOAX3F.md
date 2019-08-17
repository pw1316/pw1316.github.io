---
layout: trophy
title: "DEAD OR ALIVE Xtreme 3 Fortune"
image: http://wx1.sinaimg.cn/thumb150/bfae17b6ly1ffzo44o5f6j20sg0sgwy4
alt: "DEAD OR ALIVE Xtreme 3 Fortune"
---

<tr><td colspan="4"><p>{{ site.data.DOAX3F.Trophies.name }}</p></td></tr>

{% for item in site.data.DOAX3F.Trophies.trophy %}
{% include trophy/trophy_item.html %}
{% endfor %}
