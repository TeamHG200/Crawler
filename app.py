#!/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json, datetime
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, make_response, send_from_directory
import crawler
import sqlite3,json
import db_tool
from file_tool import FileTool


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

@app.route('/do_score', methods=['GET'])
def score():
    rid = request.args.get('review_id')
    score = request.args.get('score')
    json_res = []
    res = app.db.update_review_score(rid, score)
    return jsonify(res)

@app.route('/review_count', methods=['GET'])
def review_count():
    res = app.db.review_count()
    json_res = {
        'count' : res[0][0]
    }

    return jsonify(json_res)

@app.route('/do_crawler')
def crawler():
    gid = request.args.get('gid', '0')
    res = cw.get_review(gid)
    json_res = {
        'count' : len(res)
    }
    return jsonify(json_res)

@app.route('/get_split', methods=['GET'])
def words():
    json_res = []
    res = app.db.fetch_words()
    for r in res:
        json_res.append({
                'review_id' : r[0],
                'game_id' : r[1],
                'words' : json.loads(r[2]),
                'emotion' : json.loads(r[3])
        })
    return jsonify(json_res)


@app.route('/do_split')
def split():
    review_count = app.db.review_count()
    res = app.db.fetch_review_useful("0", str(review_count[0][0]))
    for r in res:
        sp.split(r[0], r[1], r[2])

    json_res = {
        'count' : len(res)
    }
    return jsonify(json_res)

@app.route('/get_feature')
def get_feature():
    json_res = []
    res = app.db.fetch_feature()
    for r in res:
        json_res.append({
                'review_id' : r[0],
                'game_id' : r[1],
                'feature' : json.loads(r[2]),
                'score' : json.loads(r[3])
        })

    return jsonify(json_res)

@app.route('/do_feature')
def do_feature():
    res = app.db.fetch_words()
    for r in res:
        sp.feature(r[0], r[1], json.loads(r[3]))

    json_res = {
        'count' : len(res)
    }
    return jsonify(json_res)



###
@app.route('/positive', methods=['GET', 'POST'])
def word_page():

    if request.method == 'GET':
        response = make_response(render_template('positive.html'))
        return response
    elif request.method == 'POST':
        user = UserModel(request, app.api.db)
        response = make_response(redirect(url_for('index')))
        app.auth = Auth(request, response)
        app.auth.login(user)
        app.api.new_user(user)
        return response
    else:
        return redirect(url_for('index'))



### FILE ###
@app.route('/file/<path:path>', methods = ['GET', 'POST'])
def get_file(path):
    res = ""
    ft = FileTool()
    if request.method == 'GET':
        res = ft.readFile(path)
        return res
    elif request.method == 'POST':
        content = request.files.get('file')
        if content:
            res = ft.writeFile(path, content.read())
        else:
            content = request.form.get('content')
            if content is not None:
                res = ft.writeFile(path, content)
        sp.wd.load() # reload
        return "true"
    return res




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
