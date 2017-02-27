#!/bin/env python
# -*- coding: utf-8 -*-
import os, sys, json, datetime
from functools import wraps
from flask import Flask, render_template, jsonify, request, Response, make_response, redirect, url_for
import json
import crawler

app = Flask(__name__, instance_relative_config=True)

import crawler

@app.route('/<path>')
def logout(path):
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
    app.run(host = '121.43.56.115', port = 5001, debug=True)
