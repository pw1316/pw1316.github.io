---
layout: page
title: 码海无涯，回头是岸
---

{% assign sorted_posts = site.posts | sort: 'mdate' | reverse | slice: 0, 2 %}
<div class="meta"><span>{{ site.description }}</span></div>

<table cellspacing="0" class="toc">
{% for post in site.posts %}
<tr>
<td>{% if sorted_posts contains post %}<i class="fas fa-hammer"></i>{% endif %}</td>
<td>{{ post.date | date: "%Y-%m-%d %H:%M" }}<a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></td>
</tr>
{% endfor %}
</table>

<table cellspacing="0" class="toc">
<th>{{ site.data.Ferrari.Record.name }}</th>
{% for item in site.data.Ferrari.Record.items %}
<tr>
<td>
距离<span class="pf_ps3">Scuderia Ferrari</span>的上一个
<span class="pf_ps4" display="block">{{ item.name }}</span>
已经过去了{% assign t_then = item.when | date: "%s" %}<span class="pf_psv sf_date">{{ t_then | date: "%Y-%m-%dT%H:%M:%S%z" }}</span>天，上一次发生在
<span class="pf_psp" display="block">{{ item.where }}</span>由<strong>{{ item.who }}</strong>取得
</td>
</tr>
{% endfor %}
</table>

<script>
$(".sf_date").each(function(){
    then = new Date($(this).html());
    diff = (now.getTime() - then.getTime()) / (1000 * 60 * 60 * 24);
    $(this).html(diff.toFixed(5));
});
</script>

<!-- ![My Trophy Card](https://card.psnprofiles.com/2/PW__1316.png) -->
