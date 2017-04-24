#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import urllib2
import json
import jieba
import operator
import db_tool
import jieba


class Spliter:
    def __init__(self, config):
        self.config = config
        self.db = db_tool.DB(config)

    def check_words(self, words):
        stat = {}
        for w in words:
            if w not in stat:
                stat[w] = 1
            else:
                stat[w] += 1
        sorted_words = sorted(stat.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_words[0:5]

    def split(self, review_id, game_id, review):
        words = self.check_words(list(jieba.cut(review)))
        words_json = json.dumps(words)
        self.db.update_words(review_id, game_id, words_json, "")
