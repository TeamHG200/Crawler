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
crawler = Crawler(app.config)

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
            'game_id' : r[0],
            'review_id' : r[1],
            'text' : r[2],
            'score' : r[3]
        })
    return jsonify(json_res)

@app.route('/review_count', methods=['GET'])
def review_count():
    res = app.db.review_count()
    json_res = {
        'count' : res[0][0]
    }

    return jsonify(json_res)

@app.route('/<path>')
def crawler(path):
    html = "<table border=\"1\"><tbody>"
    res = crawler.get_review(path)
    for r in res:
        html += "<tr>"
        html += "<td>" + r[0] + "</td>"
        html += "<td><table border=\"1\"><tbody>"
        for w in r[1]:
            html += '<tr><td>'+ w[0] +'</td>'
            html += '<td>'+ str(w[1]) +'</td></tr>'
        html += "</tbody></table></td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

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
