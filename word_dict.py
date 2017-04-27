#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import urllib2
import json
import jieba
import operator
import db_tool
import jieba

class Word:
    def __init__(self):
        self.load()

    def load(self):

        negative1=open('ntusd/ntusd-negative.txt').readlines()
        positive1=open('ntusd/ntusd-positive.txt').readlines()

        self.negative = {}
        for line in negative1:
            w = line[:-2]
            w.strip()
            self.negative[w] = -1

        self.positive = {}
        for line in positive1:
            w = line[:-2]
            w.strip()
            self.positive[w] = 1


    def check(self,word):
        if word in self.positive:
            return 1

        if word in self.negative:
            return -1

        return 0
