---
layout: trophy
title: "Assassin's Creed® Odyssey"
image: http://wx1.sinaimg.cn/thumb150/bfae17b6ly1fsl2laexs5j206o06ogon
alt: "Assassin's Creed® Odyssey"
---

<tr><td colspan="4"><p>{{ site.data.ACOD.Trophies.name }}</p></td></tr>

{% for item in site.data.ACOD.Trophies.trophy %}
{% include trophy_item.html %}
{% endfor %}
