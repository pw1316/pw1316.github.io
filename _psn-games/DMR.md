---
layout: trophy
title: "DJMAX RESPECT"
image: http://wx1.sinaimg.cn/thumb150/bfae17b6ly1fgve8edseqj21kw0u00uw
alt: "DJMAX RESPECT"
---

<tr><td colspan="4"><p>{{ site.data.DMR.Trophies.name }}</p></td></tr>

{% for item in site.data.DMR.Trophies.trophy %}
{% include trophy_item.html %}
{% endfor %}
