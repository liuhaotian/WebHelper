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
Simple HTML5 player for youtube Flash-only videos

###Example:
`http://127.0.0.1:5000/youtube/m3ROQJ-Vvy4` will render a html5 player for `http://www.youtube.com/watch?v=m3ROQJ-Vvy4`

###Intergrate with privoxy:
```
{+redirect{s@^http://www.youtube.com/watch\?v=([\w\d_-]*)$@http://127.0.0.1:5000/youtube/$1@}}
www.youtube.com/watch\?v=.*
```

###Use javascript bookmarklet:
```
javascript:var form=document.createElement("form");form.setAttribute("method","POST");form.setAttribute("action","http://127.0.0.1:5000/youtube/"+ytplayer.config.args.video_id);var hiddenField=document.createElement("input");hiddenField.setAttribute("value",btoa(ytplayer.config.args.url_encoded_fmt_stream_map));hiddenField.setAttribute("name","video_data");form.appendChild(hiddenField);document.body.appendChild(form);form.submit();
```