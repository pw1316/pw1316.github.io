---
layout: trophy
title: "Marvel's Spider-Man"
image: http://wx1.sinaimg.cn/thumb150/43823ba4gw1f4wytz5lfoj21hc0u0jz9
alt: "Marvel's Spider-Man"
---

<tr><td colspan="4"><p>{{ site.data.SPIDERMAN.Trophies.name }}</p></td></tr>

{% for item in site.data.SPIDERMAN.Trophies.trophy %}
{% include trophy_item.html %}
{% endfor %}
