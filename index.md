---
layout: page
title: 码海无涯，回头是岸
showbar: true
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

<!-- ![My Trophy Card](https://card.psnprofiles.com/2/PW__1316.png) -->
