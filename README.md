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

RSS proxy
---------
Proxy the base64 encoded rss source and use content fetcher to generate the full-text content

###Format:
`http://127.0.0.1:5000/rss/<base64encoded url>?root_selector=<base64encoded selector>&del_bs_selectors=<base64encoded selector>,<base64encoded selector>...`

###Example:
For rss source `http://cn.engadget.com/rss.xml`, `'.post-body'` as root selector, `['script']` as the del_bs_selectors,
`http://localhost:5000/rss/aHR0cDovL2NuLmVuZ2FkZ2V0LmNvbS9yc3MueG1s?root_selector=LnBvc3QtYm9keQ==&del_bs_selectors=c2NyaXB0` will return the full text engadget rss

Content fetcher
---------------
Fetch the base64 encoded url and filter the content by beautifulsoup selector

###Format:
`http://127.0.0.1:5000/fetcher/<base64encoded url>?root_selector=<base64encoded selector>&del_bs_selectors=<base64encoded selector>,<base64encoded selector>...`

###Example:
For url `http://www.cnn.com`, `[#cnnMainPage]` as root, `['script', '#cnn_hdr']` as filter, `http://localhost:5000/fetcher/aHR0cDovL3d3dy5jbm4uY29t?root_selector=I2Nubk1haW5QYWdl&del_bs_selectors=c2NyaXB0,I2Nubl9oZHI=` will return the cnn website body without javascript and header

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

If you want to set the video watched:
```
javascript:var form=document.createElement("form");form.setAttribute("method","POST");form.setAttribute("action","http://127.0.0.1:5000/youtube/"+ytplayer.config.args.video_id);var hiddenField=document.createElement("input");hiddenField.setAttribute("value",btoa(ytplayer.config.args.url_encoded_fmt_stream_map));hiddenField.setAttribute("name","video_data");form.appendChild(hiddenField);hiddenField=document.createElement("input");hiddenField.setAttribute("value",btoa("http://www.youtube.com/user_watch?noflv=1&html5=1&video_id="+ytplayer.config.args.video_id+"&plid="+ytplayer.config.args.plid+"&referrer&fmt=18&ptk=youtube_none&skl=false&ucid="+ytplayer.config.args.ucid+"&ns=yt&el=detailpage&fexp="+ytplayer.config.args.fexp));hiddenField.setAttribute("name","watch_url");form.appendChild(hiddenField);document.body.appendChild(form);form.submit();
```
