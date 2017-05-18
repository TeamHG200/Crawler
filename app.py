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
    app.db.remove_words()
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
        useful = ""
        is_useful = app.db.is_useful(r[0])
        if len(is_useful) == 1:
           useful = is_useful[0][0]
        json_res.append({
                'review_id' : r[0],
                'game_id' : r[1],
                'feature' : r[2],
                'score' : json.loads(r[3]),
                'useful' : useful
        })

    return jsonify(json_res)

@app.route('/do_train')
def do_train():
    json_res = []
    res = app.db.fetch_feature()
    f_train = open('feature.train.csv', 'w')
    f_test  = open('feature.test.csv', 'w')
    pos = len(res)*0.8

    for r in res:
        useful = ""
        line = ""
        is_useful = app.db.is_useful(r[0])
        pos -= 1
        if len(is_useful) == 1:
            useful = is_useful[0][0]
            score = json.loads(r[3])
            line = str(useful) + '\t1:' + str(score['1'])  + '\t2:' + str(score['2'])
            if pos >= 0:
                f_train.write(line+'\n')
            else:
                f_test.write(line+'\n')

    f_test.close()
    f_train.close()

    t = os.popen('svm-train -c 100 -t 0 feature.train.csv')
    p = os.popen('svm-predict feature.test.csv feature.train.csv.model feature.test.predict')

    return jsonify({
        'rate' : p.read(),
        'train_count': len(res)*0.8,
        'test_count' : len(res)*0.2
    })

@app.route('/do_feature')
def do_feature():

    minium_x = 0
    maxium_x = 0

    minium_y = 0
    maxium_y = 0

    scores = {}
    app.db.remove_feature()
    res = app.db.fetch_words()
    for r in res:
        score1, score2 = sp.feature(r[0], r[1], json.loads(r[3]))

        if score1 < minium_x:
            minium_x = score1
        if score1 > maxium_x:
            maxium_x = score1

        if score2 < minium_y:
            minium_y = score2
        if score2 > maxium_y:
            maxium_y = score2

        scores[r[0]] = [r[1], score1, score2]

    scale_x = float(maxium_x-minium_x)/1130
    scale_y = float(maxium_y-minium_y)/600

    for r in scores.keys():
        score1 = scores[r][1]
        score2 = scores[r][2]
        score1 = float(score1-minium_x)/scale_x
        score2 = float(score2-minium_y)/scale_y
        print(r, scores[r][0], score1, score2)
        app.db.update_feature(r, scores[r][1], "", json.dumps({
            "1":score1,
            "2":score2
        }))

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
    #ip="121.43.56.115"
    app.run(host = ip, port = app.config['PORT'], debug=True)
