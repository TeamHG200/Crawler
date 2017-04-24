#!/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json, datetime
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, make_response, send_from_directory
import crawler
import sqlite3,json
import db_tool


#from etc import config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('db.config.Config')
app.db = db_tool.DB(app.config)

from crawler import Crawler
cw = Crawler(app.config)

from split import Spliter
sp = Spliter(app.config)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/reviews', methods=['GET'])
def reviews():
    s = request.args.get('s', '0')
    n = request.args.get('n', '20')
    json_res = []
    res = app.db.fetch_review(s, n)
    for r in res:
        json_res.append({
                'review_id' : r[0],
                'game_id' : r[1],
                'text' : r[2],
                'score' : r[3]
        })
    return jsonify(json_res)

@app.route('/words', methods=['GET'])
def words():
    json_res = []
    res = app.db.fetch_words()
    for r in res:
        json_res.append({
                'review_id' : r[0],
                'game_id' : r[1],
                'words' : json.loads(r[2]),
                'emotion' : r[3]
        })
    return jsonify(json_res)

@app.route('/review_count', methods=['GET'])
def review_count():
    res = app.db.review_count()
    json_res = {
        'count' : res[0][0]
    }

    return jsonify(json_res)

@app.route('/crawler')
def crawler():
    gid = request.args.get('gid', '0')
    res = cw.get_review(gid)
    json_res = {
        'count' : len(res)
    }
    return jsonify(json_res)

@app.route('/split')
def split():
    review_count = app.db.review_count()
    res = app.db.fetch_review("0", str(review_count[0][0]))
    for r in res:
        sp.split(r[0], r[1], r[2])

    json_res = {
        'count' : len(res)
    }
    return jsonify(json_res)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

# init db
    with app.app_context():
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = sqlite3.connect(app.config['DATABASE_URI'])
            g.sqlite_db.row_factory = sqlite3.Row
        db = g.sqlite_db
        with app.open_resource(app.config['DATABASE_SCHEMA'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    try:
        hostname = socket.getfqdn(socket.gethostname())
        ip = socket.gethostbyname(hostname)
    except Exception, e:
        ip = "127.0.0.1"

    app.run(host = ip, port = app.config['PORT'], debug=True)
