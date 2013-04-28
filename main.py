#!/usr/bin/env python


import re

from urlparse import urlparse

import requests

from flask import Flask, redirect


app = Flask(__name__)
session = requests.session()
session.keep_alive = False
session.headers.update({'User-Agent': 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'})


@app.route("/instagram/<path:url>")
def instagram(url):
    if not urlparse(url).scheme:
        url = 'http://' + url
    resp = session.get(url)
    image_url = re.search(r'http://[\w]*image[\d]*.ak.instagram.com/[\d\w_]*\.jpg', resp.content).group()
    return redirect(image_url, 301)


if __name__ == "__main__":
    app.run()