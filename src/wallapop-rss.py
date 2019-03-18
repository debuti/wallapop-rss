#!/usr/bin/env python3
'''
Script to convert json data to rss data. Thanks to https://salvacarrion.github.io/data/analysis/2018/05/17/mining-in-wallapop.html for the previous work
'''

##TODO:

# Imports
import sys
import os
import requests
import json
import time
import html
import urllib.parse
from flask import Flask #pip3 install Flask
from flask import flash, redirect, render_template, request, session, abort, Response, send_from_directory

# Global variables
app = Flask(__name__)


# Class declarations


# Function declarations
def json2rss(dlout):
    '''Turns the json returned by wallapop to a rss 2.0 feed'''
    rss = '<?xml version="1.0"?><rss version="2.0">' + "\n";
    rss += '<channel><title>Wallapop RSS: \"' + dlout["kws"] + '\"</title>' + "\n";
    rss += '<link>' + dlout["query"] + '</link>' + "\n";
    rss += '<description>Wallapop RSS: \"' + dlout["kws"] + '\"</description>' + "\n";
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

#def download(host, kws, dist = "2000", lat = "40.456065", lng = "-3.715892", minp = "0.0", maxp = "999999999"):
def download(host, kws, dist, minp, maxp, lat, lng):
    '''
    '''
    if not lat or not lng: raise ValueError('Latitude and Longitude are needed')

    ENDPOINT='https://es.wallapop.com/rest/items?_p=1&kws={}&publishDate=any&orderBy=creationDate&orderType=asc'
    q = ENDPOINT.format(urllib.parse.quote_plus(kws)) + \
        ("&dist="+dist if dist else "") + \
        ("&minPrice="+minp if minp else "") + \
        ("&maxPrice="+maxp if maxp else "") + \
        ("&latitude="+lat if lat else "") + \
        ("&longitude="+lng if lng else "")
    print(q)
    r = requests.get(q, headers = {'cookie': 'searchLat='+lat+'; searchLng='+lng+';'})
    #r = requests.get(q)
    if (r.status_code != 200 or
        r.headers['content-type'] != 'application/json;charset=UTF-8'):
      raise RuntimeError("Unable to download wallapop item list");
    return {"query" : html.escape(q),
            "host" : host,
            "kws" : kws,
            "dist" : dist,
            "lat" : lat,
            "lng" : lng,
            "result" : r.content};

@app.route("/search")
def search():
	return Response(json2rss(download(request.base_url,
                                      request.args.get('kws'),
                                      request.args.get('dist'),
                                      request.args.get('minPrice'),
                                      request.args.get('maxPrice'),
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

