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
<span class="pf_ps3">Scuderia Ferrari</span>'s previous
<span class="pf_ps4" display="block">{{ item.name }}</span>was
<span class="pf_psv sf_date">{% assign t_then = item.when | date: "%s" %}{{ t_then | date: "%Y-%m-%dT%H:%M:%S%z" }}</span>days ago, achieved in
<span class="pf_psp" display="block">{{ item.where }}</span>by
<strong>{{ item.who }}</strong>
</td>
</tr>
{% endfor %}
</table>

<script>
$(".sf_date").each(function(){
    then = new Date($(this).html());
    diff = (now.getTime() - then.getTime()) / (1000 * 60 * 60 * 24);
    $(this).html(Math.floor(diff));
});
</script>

<!-- ![My Trophy Card](https://card.psnprofiles.com/2/PW__1316.png) -->
