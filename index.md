<h1>{{ page.title }}</h1>
<p>最新文章</p>
<ul>
    {% for post in site.posts %}
    <li>{{ post.date | date_to_string }} <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>

![My Trophy Card](http://psnine.com/card/pw__1316)

### Welcome to GitHub Pages.

This automatic page generator is the easiest way to create beautiful pages for all of your projects. Author your page content here [using GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/), select a template crafted by a designer, and publish. After your page is generated, you can check out the new `gh-pages` branch locally. If you’re using GitHub Desktop, simply sync your repository and you’ll see the new branch.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/pages) or [contact support](https://github.com/contact) and we’ll help you sort it out.

Someone@[Me](https://github.com/pw1316)

CopyRight(C) Joker Yough 2016-2018
