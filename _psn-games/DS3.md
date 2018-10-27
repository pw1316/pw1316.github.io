---
layout: trophy
title: "Dark Souls 3 wiki"
image: https://trophy01.np.community.playstation.net/trophy/np/NPWR07897_00_00B1B88693A993473272413EDB83CC197E895B34D1/E1FA01E8C2DBAAEC2AF046BDE73D6E35DAA36DBA.PNG
alt: DS3
---

<tr><td colspan="4"><p>{{ site.data.DarkSouls3.Trophies.name }}</p></td></tr>

{% for item in site.data.DarkSouls3.Trophies.trophy %}
{% include trophy_item.html %}
{% endfor %}
