#!/usr/bin/env python3
'''
Script to convert json data to rss data
'''

##TODO:

# Imports
import sys
import os
import requests
import json
import time
from flask import Flask #pip3 install Flask
from flask import flash, redirect, render_template, request, session, abort, Response, send_from_directory

# Global variables
app = Flask(__name__)


# Class declarations


# Function declarations
def json2rss(dlout):
    '''Turns the json returned by wallapop to a rss 2.0 feed'''
    rss = '<?xml version="1.0"?><rss version="2.0">' + "\n";
    rss += '<channel><title>Wallapop RSS</title>' + "\n";
    rss += '<link>'+dlout["host"]+'</link>' + "\n";
    rss += '<description>Wallapop RSS for kws \"'+dlout["kws"]+'\"</description>' + "\n";
    json_object = json.loads(dlout["result"])

    for item in json_object['items']:
        rss += "<item>" + "\n"
        rss += "<title>(" + item['price'] + ") " + item['title'] + "</title>" + "\n"
#       rss += "<pubDate>" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['publishDate'])) + "</pubDate>" + "\n"
        rss += "<guid isPermaLink='false'>" + item['itemUUID'] + "</guid>" + "\n"
        rss += "<link>https://es.wallapop.com/item/" + item['url']  + "</link>" + "\n"
        rss += "<description>" + item['description'] + "\nPrice: " + item['price'] + "</description>" + "\n"
        rss += "</item>" + "\n"

    rss += "</channel></rss>"
    return rss

def download(host, kws, dist = 2000, lat = 40.456065, long = -3.715892):
    '''
    '''
    ENDPOINT='https://es.wallapop.com/rest/items?_p=1&kws={}&dist={}&latitude={}&longitude={}&publishDate=any&orderBy=creationDate&orderType=asc'
    q = ENDPOINT.format(kws, dist, lat, long)
    r = requests.get(q)
    if (r.status_code != 200 or
        r.headers['content-type'] != 'application/json;charset=UTF-8'):
      return "Unable to download wallapop item list";
    return {"query" : q,
            "host" : host,
            "kws" : kws,
            "dist" : dist,
            "lat" : lat,
            "long" : long,
            "result" : r.content};

@app.route("/search")
def search():
	return Response(json2rss(download(request.base_url,
                                      request.args.get('kws'),
                                      request.args.get('dist'),
                                      request.args.get('lat'),
                                      request.args.get('long'))),
                    mimetype='application/rss+xml')

@app.route("/")
def hello():
    return 

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Main body
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)

