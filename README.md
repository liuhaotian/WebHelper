WebHelper
=========

A web helper to make my life easier


Features
========

Instagram redirector
--------------------
Use 301 redirect to only return the actual image url

###Example:
`http://127.0.0.1:5000/instagram/http://instagram.com/p/Yo2LffFm0U/` will return the real image url ` http://distilleryimage0.ak.instagram.com/2621d28aafcc11e2bb6122000a1f9d92_7.jpg`

###Intergrate with privoxy:
```
{+redirect{s@^(.*)$@http://127.0.0.1:5000/instagram/$1@}}
instagram.com/p/.*
```

Youtube player
--------------
###Example:
`http://127.0.0.1:5000/youtube/m3ROQJ-Vvy4` will render a html5 player for `http://www.youtube.com/watch?v=m3ROQJ-Vvy4`

###Intergrate with privoxy:
```
{+redirect{s@^http://www.youtube.com/watch\?v=([\w\d_-]*)$@http://127.0.0.1:5000/youtube/$1@}}
www.youtube.com/watch\?v=.*
```