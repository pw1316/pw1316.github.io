import os

wallpaperFile = open('../wallpaper.html', 'wb')
wallpaperFile.write(b'<!DOCTYPE html>\n')
wallpaperFile.write(b'<html>\n')
wallpaperFile.write(b'  <head>\n')
wallpaperFile.write(b'    <meta charset="UTF-8">\n')
wallpaperFile.write(b'    <title>Joker Yough\'s Wallpaper</title>\n')
wallpaperFile.write(b'    <meta name="viewport" content="width=device-width, initial-scale=1">\n')
wallpaperFile.write(b'    <link rel="stylesheet" type="text/css" href="/stylesheets/normalize.css" media="screen">\n')
wallpaperFile.write(b'    <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700" rel="stylesheet" type="text/css">\n')
wallpaperFile.write(b'    <link rel="stylesheet" type="text/css" href="/stylesheets/stylesheet.css" media="screen">\n')
wallpaperFile.write(b'    <link rel="stylesheet" type="text/css" href="/stylesheets/github-light.css" media="screen">\n')
wallpaperFile.write(b'    <link rel="Shortcut Icon" href="/src/icon.png">\n')
wallpaperFile.write(b'  </head>\n')
wallpaperFile.write(b'  <body>\n')
wallpaperFile.write(b'    <section class="page-header">\n')
wallpaperFile.write(b'      <h1 class="project-name">Joker Yough\'s Wallpaper</h1>\n')
wallpaperFile.write(b'      <h2 class="project-tagline"><a href="/index.html" style="color: #FFFFFF;">Back</a></h2>\n')
wallpaperFile.write(b'    </section>\n')
wallpaperFile.write(b'    <section class="main-content">\n')
wallpaperFile.write(b'      <table>\n')

if os.path.exists('../Wallpapers'):
    for parent, dirs, files in os.walk('../Wallpapers'):
        for image in files:
            wallpaperFile.write(b'        <tr><td><a href = "../Wallpapers/' + image + b'"><img src = "../Wallpapers/' + image + b'" alt = "IMG"></a></td></tr>\n') 

wallpaperFile.write(b'      </table>\n')
wallpaperFile.write(b'      <footer class="site-footer">\n')
wallpaperFile.write(b'        <p class="site-footer-credits">Someone<a href="https://github.com/pw1316">@Me</a></p>\n')
wallpaperFile.write(b'        <p class="site-footer-credits">CopyRight(C) Joker Yough 2016-2017</p>\n')
wallpaperFile.write(b'      </footer>\n')
wallpaperFile.write(b'    </section>\n')
wallpaperFile.write(b'  </body>\n')
wallpaperFile.write(b'</html>\n')
wallpaperFile.close()
