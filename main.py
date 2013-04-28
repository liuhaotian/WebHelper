#!/usr/bin/env python


import re

from urlparse import urlparse

import requests

from flask import Flask, redirect


app = Flask(__name__)


@app.route("/instagram/<path:url>")
def instagram(url):
    if not urlparse(url).scheme:
        url = 'http://' + url
    resp = requests.get(url)
    image_url = re.search(r'http://[\w]*image[\d]*.ak.instagram.com/[\d\w_]*\.jpg', resp.content).group()
    return redirect(image_url)


if __name__ == "__main__":
    app.run()