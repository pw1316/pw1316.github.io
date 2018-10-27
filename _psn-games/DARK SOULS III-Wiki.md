---
layout: trophy
title: "Dark Souls 3 wiki"
image: https://trophy01.np.community.playstation.net/trophy/np/NPWR13822_00_00E63FD8AB71E35431D284C875D26290C020A6ED1A/19162490E22A23B0AF72FDAE3482D1F36188564A.PNG
alt: DS3
hide: true
---

<tr><td colspan="4"><p>DARK SOULS III</p><em><span class="text-platinum">白1</span><span class="text-gold">金3</span><span class="text-silver">银13</span><span class="text-bronze">铜26</span><span class="text-strong">总43</span></em></td></tr>

{% for item in site.psn-games %}
<tr><td>{{ item.url }}</td></tr>
{% endfor %}

{% for item in site.data.DarkSouls3.Trophies %}
<tr id="{{ item.id }}">
<td colspan="4">
<p><em class="h-p">{{ item.id }}</em><span class="{{ item.type }}">{{ item.name }}</span></p>
<em class="text-gray">{{ item.desc }}</em>
</td>
</tr>
{% endfor %}
