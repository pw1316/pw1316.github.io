---
layout: trophy
title: "Red Dead Redemption 2"
image: http://wx1.sinaimg.cn/thumb150/bfae17b6ly1fwk9ufgsfvj206o06ognp
alt: "Red Dead Redemption 2"
---

<tr><td colspan="4"><p>{{ site.data.RDR2.Trophies.name }}</p></td></tr>

{% for item in site.data.RDR2.Trophies.trophy %}
{% include trophy_item.html %}
{% endfor %}
