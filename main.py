#!/usr/bin/env python


import re
import json

from urlparse import urlparse, parse_qs

import requests

from flask import Flask, redirect


app = Flask(__name__)
session = requests.session()
session.keep_alive = False
#session.headers.update({'User-Agent': 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'})


@app.route("/instagram/<path:url>")
def instagram(url):
    if not urlparse(url).scheme:
        url = 'http://' + url
    resp = session.get(url)
    image_url = re.search(r'http://[\w]*image[\d]*.ak.instagram.com/[\d\w_]*\.jpg', resp.content).group()
    return redirect(image_url, 301)


@app.route('/youtube/<string:video_id>')
def youtube(video_id):
    url = 'http://www.youtube.com/watch?v={}'.format(video_id)
    resp = session.get(url)

    video_data = re.search(r'url_encoded_fmt_stream_map[\W]*([^\'"]*)', resp.content)
    video_data = video_data.groups()
    video_data = video_data[0]
    video_data = video_data.replace(r'\u0026', u'\u0026')
    video_data = video_data.split(',')
    video_data = map(parse_qs, video_data)
    video_data = [{k:d[k][0] for k in d} for d in video_data]
    for video in video_data:
        video['type'] = video['type'].replace('"', '')

    qualities = {'small': 1, 'medium': 2, 'large': 3, 'hd720': 4, 'hd1080': 5}
    qualities_index = {v:k for k,v in qualities.items()}
    best_quality = qualities_index[max(map(lambda d: qualities[d['quality']] , video_data))]

    ret = []
    ret.append(r'<video controls style=" position:fixed;top:0;left:0;bottom:0;right:0;height:100%;width:100%;">')
    for quality in sorted(qualities, key=lambda x:qualities[x], reverse=True):
        for video in video_data:
            if video['quality'] == quality:
                ret.append("<source src='{url}&signature={sig}' type='{type}'>".format(**video))
    ret.append('</video>')
    return ''.join(ret)

if __name__ == "__main__":
    app.run()