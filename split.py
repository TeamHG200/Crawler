#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import urllib2
import json
import jieba
import operator
import db_tool
import jieba
from word_dict import Word

ch = [',', '.', '。', '～', '，', ')', '(', '？', '?', '！', '!', '（', '）',
      '【', '】', '@', '‘', '’', '“', '”', '\'', ':', ';', '：', '；' , '/',
      '-', '+', '*', ' ', '=','&', '・', '……', '…', '`', '| ', '￣', '一', '',
      '♥', '$']

clean = re.compile(u'^[\u4e00-\u9fa5A-Za-z]')
jieba.load_userdict('ntusd/ntusd-negative.txt')
jieba.load_userdict('ntusd/ntusd-positive.txt')

class Spliter:
    def __init__(self, config):
        self.config = config
        self.db = db_tool.DB(config)
        self.wd = Word()

    def valid_word(self, word):
        return re.sub(clean,'', word)

    def check_words(self, words):
        stat = []
        for w in words:
#            w = self.valid_word(w)
            if w in ch:
                continue


#            if self.wd.check(w) == 0:
#                continue

            stat.append(w)
#        sorted_words = sorted(stat.items(), key=operator.itemgetter(1), reverse=True)
        return stat

    def split(self, review_id, game_id, review):
        words = self.check_words(list(jieba.cut(review)))
        words_json = json.dumps(words)
        self.db.update_words(review_id, game_id, words_json, "")
