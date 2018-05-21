---
layout: page
title: 文章列表
---

<ul>
    {% for post in site.posts %}
    <li>{{ post.date | date_to_string }} <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>

![My Trophy Card](http://psnine.com/card/pw__1316)
