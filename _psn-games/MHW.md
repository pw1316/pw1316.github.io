---
layout: trophy
title: " Monster Hunter World"
image: http://wx1.sinaimg.cn/thumb150/bfae17b6ly1fgjip3ptakj21hc0u01gt
alt: " Monster Hunter World"
---

<tr><td colspan="4"><p>{{ site.data.MHW.Trophies.name }}</p></td></tr>

{% for item in site.data.MHW.Trophies.trophy %}
{% include trophy/trophy_item.html %}
{% endfor %}
