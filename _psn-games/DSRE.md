---
layout: trophy
title: "DARK SOULS™ REMASTERED"
image: http://wx1.sinaimg.cn/thumb150/bfae17b6ly1fga1zm4p3aj206o06odha
alt: "DARK SOULS™ REMASTERED"
---

<tr><td colspan="4"><p>{{ site.data.DSRE.Trophies.name }}</p></td></tr>

{% for item in site.data.DSRE.Trophies.trophy %}
{% include trophy_item.html %}
{% endfor %}
