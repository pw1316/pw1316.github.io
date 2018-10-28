---
layout: trophy
title: "初音未來 Project DIVA Future Tone"
image: http://wx1.sinaimg.cn/thumb150/bfae17b6ly1ffzoo6ehj3j20sg0sg4qp
alt: "初音未來 Project DIVA Future Tone"
---

<tr><td colspan="4"><p>{{ site.data.DIVAFT.Trophies.name }}</p></td></tr>

{% for item in site.data.DIVAFT.Trophies.trophy %}
{% include trophy_item.html %}
{% endfor %}
