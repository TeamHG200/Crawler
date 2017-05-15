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
        negative2=open('ntusd/ntusd-negative-extend.txt').readlines()
        positive2=open('ntusd/ntusd-positive-extend.txt').readlines()
        adj=open('ntusd/ntusd-adj.txt').readlines()
        adv=open('ntusd/ntusd-adv.txt').readlines()

        self.negative = {}
        self.positive = {}

        for line in positive1:
            w = line[:-1]
            w.strip()
            self.positive[unicode(w)] = 1

        for line in negative1:
            w = line[:-1]
            w.strip()
            self.negative[unicode(w)] = -1


        self.negative2 = {}
        self.positive2 = {}

        for line in positive2:
            w = line[:-1]
            w.strip()
            self.positive2[unicode(w)] = 1

        for line in negative2:
            w = line[:-1]
            w.strip()
            self.negative2[unicode(w)] = -1

        self.adj = {}
        for line in adj:
            w = line[:-1]
            w.strip()
            self.adj[unicode(w)] = 1

        self.adv = {}
        for line in adv:
            w = line[:-1]
            w.strip()
            self.adv[unicode(w)] = 1


    def check(self,word):

        if word in self.positive2:
            return 5

        if word in self.negative2:
            return -5

        if word in self.adj:
            return 20

        if word in self.adv:
            return -10

        if word in self.positive:
            return 1

        if word in self.negative:
            return -1

        return 0
