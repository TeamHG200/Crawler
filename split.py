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
      '♥', '$', ' ']

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



    def add_score(self, words, w, score):
        if w not in words:
            words[w] = score
        else:
            words[w] += score



    def check_words(self, words):
        stat = []
        emotion_word = {}
        last = ""
        last_score = 0
        for w in words:
            if w in ch or len(w) == 1:
                continue

            score = self.wd.check(w)
            if score != 0:
                if last_score >= 20 or last_score <= -20:
                    if score == 20 or score == -20:
                        last_score = score * last_score
                        last = '(' + last + ')' + w
                    else:
                        self.add_score(emotion_word, '('+last+')'+w, score*last_score)
                        last = w
                        last_score = score
                elif not last_score == 20 and not last_score == -20:
                    self.add_score(emotion_word, w, score)
                    last = w
                    last_score = score
            else:
                last = w
                last_score = 0

            stat.append(w)

        return stat, emotion_word

    def split(self, review_id, game_id, review):
        words, emotions = self.check_words(list(jieba.cut(review)))
        words_json = json.dumps(words)
        emotions_json = json.dumps(emotions)
        self.db.update_words(review_id, game_id, words_json, emotions_json)


    def feature(self, review_id, game_id, words):

        scores1 = 0
        scores2 = 0
        for w in words.keys():
            score = words[w]
            if score < 0:
                scores1 += score
            else:
                scores1 += score

        scores2 = scores1*0.5
        feature = {
            "1": scores1,
            "2": scores2
        }

        self.db.update_feature(review_id, game_id, "", json.dumps(feature))
        return scores1, scores2
