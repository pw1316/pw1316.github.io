---
layout: page
---

<h1>{{ page.title }}</h1>
<p>文章列表</p>
<ul>
    {% for post in site.posts %}
    <li>{{ post.date | date_to_string }} <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>
<img src="http://psnine.com/card/pw__1316" alt="My Trophy Card">
