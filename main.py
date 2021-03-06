#!/usr/bin/env python


import re
import json
import base64

from time import mktime
from datetime import datetime
from urlparse import urlparse, parse_qs, urljoin

import requests
import feedparser

from bs4 import BeautifulSoup
from flask import Flask, redirect, request, url_for, make_response
from werkzeug.contrib.atom import AtomFeed


app = Flask(__name__)
session = requests.session()
session.keep_alive = False
# session.headers.update({'User-Agent': 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'})


@app.route("/rss/<path:url>")
def rss(url):
    url = base64.b64decode(url)
    d = feedparser.parse(url)
    feed = AtomFeed(d.feed.title, feed_url=url, url=d.feed.link)
    replace_old = request.args.get('replace_old')
    if replace_old:
        replace_old = base64.b64decode(replace_old)
    replace_new = request.args.get('replace_new')
    if replace_new:
        replace_new = base64.b64decode(replace_new)
    for entry in d.entries:
        updated = datetime.fromtimestamp(mktime(entry.updated_parsed)) if hasattr(entry, 'updated_parsed') else None
        published = datetime.fromtimestamp(mktime(entry.published_parsed)) if hasattr(entry, 'published_parsed') else None
        entry_url = entry.link
        if replace_old and replace_new:
            entry_url = entry_url.replace(replace_old, replace_new)
        entry_url = base64.b64encode(entry_url)
        entry_content = fetcher(entry_url)
        feed.add(entry.title, entry_content,
            url=entry.link,
            id=entry.id,
            updated=updated,
            published=published)
    return feed.get_response()


@app.route("/api/proxy/<path:url>")
def proxy(url):
    headers = {'User-Agent': request.headers.get('user-agent')}
    resp = session.get(url, headers=headers, verify=False)
    if 'html' in resp.headers.get('content-type'):
        soup = BeautifulSoup(resp.content)
        [s.extract() for s in soup.find_all('script')]

        # fix src and href
        for attr in ['src', 'href']:
            tags = soup.find_all(**{attr:True})
            for tag in tags:
                u = urljoin(resp.url, tag[attr])
                tag[attr] = url_for('proxy', url=u)

        response = make_response(unicode(soup))
    else:
        response = make_response(resp.content)
    response.headers['content-type'] = resp.headers.get('content-type')
    return response


@app.route("/instagram/<path:url>")
def instagram(url):
    if not urlparse(url).scheme:
        url = 'http://' + url
    resp = session.get(url)
    image_url = re.search(r'http://[\w]*image[\d]*.ak.instagram.com/[\d\w_]*\.jpg', resp.content).group()
    return redirect(image_url, 301)


@app.route("/fetcher/<path:url>")
def fetcher(url):
    url = base64.b64decode(url)
    resp = session.get(url)
    soup = BeautifulSoup(resp.content)
    root_selector = request.args.get('root_selector')
    if root_selector:
        root_selector = base64.b64decode(root_selector)
        soup = soup.select(root_selector)[0]

    del_bs_selectors = request.args.get('del_bs_selectors')
    if del_bs_selectors:
        del_bs_selectors = del_bs_selectors.split(',')
        for selector in del_bs_selectors:
            [s.extract() for s in soup.select(base64.b64decode(selector))]
    return unicode(soup)


@app.route('/youtube/<string:video_id>', methods=['GET', 'POST'])
def youtube(video_id):
    watch_url = ''
    if request.method == 'GET':
        url = 'http://www.youtube.com/watch?v={}'.format(video_id)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.29.13 (KHTML, like Gecko) Version/6.0.4 Safari/536.29.13'}
        resp = session.get(url, headers=headers)
        video_data = re.search(r'url_encoded_fmt_stream_map[\W]*([^\'"]*)', resp.content)
        video_data = video_data.groups()
        video_data = video_data[0]
    else:
        video_data = request.form['video_data']
        video_data = base64.b64decode(video_data)
        watch_url = base64.b64decode(request.form['watch_url']) if 'watch_url' in request.form else ''

    video_data = video_data.replace(r'\u0026', u'\u0026')
    video_data = video_data.split(',')
    video_data = map(parse_qs, video_data)
    video_data = [{k:d[k][0] for k in d} for d in video_data]
    for video in video_data:
        video['type'] = video['type'].replace('"', '')
        if 's' in video and 'sig' not in video:
             video['sig'] = video['s']
        if 'sig' in video and 'signature' not in video['url']:
            video['url'] += '&signature={sig}'.format(video['sig'])

    qualities = {'small': 1, 'medium': 2, 'large': 3, 'hd720': 4, 'hd1080': 5}
    qualities_index = {v:k for k,v in qualities.items()}
    best_quality = qualities_index[max(map(lambda d: qualities[d['quality']] , video_data))]

    ret = []
    ret.append(r'<video controls style=" position:fixed;top:0;left:0;bottom:0;right:0;height:100%;width:100%;">')
    for quality in sorted(qualities, key=lambda x:qualities[x], reverse=True):
        for video in video_data:
            if video['quality'] == quality:
                ret.append("<source src='{url}' type='{type}'>".format(**video))
    ret.append('</video>')
    ret.append('<img src="{watch_url}" style="visibility:hidden">'.format(watch_url=watch_url))
    return ''.join(ret)

if __name__ == "__main__":
    app.run()
