#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import urllib2
import json
import operator
import db_tool

base_url = 'http://steamcommunity.com/app/'
suffix = '?start_offset=%s&day_range=30&filter=summary&language=schinese&review_type=all&purchase_type=all&review_beta_enabled=0'


suffix = "/homecontent/?userreviewsoffset=30&p=4&workshopitemspage=4&readytouseitemspage=4&mtxitemspage=4&itemspage=4&screenshotspage=4&videospage=4&artpage=4&allguidepage=4&webguidepage=4&integratedguidepage=4&discussionspage=4&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid=438490&appHubSubSection=10&appHubSubSection=10&l=schinese&filterLanguage=default&searchText=&forceanon=1"

class Crawler:
    def __init__(self, config):
        self.config = config
        self.db = db_tool.DB(config)

    def make_suffix(self, appid, page):
        suffix = ("/homecontent/?userreviewsoffset=%d"\
                  "&p=%d"\
                  "&workshopitemspage=%d"\
                  "&readytouseitemspage=%d"\
                  "&mtxitemspage=%d"\
                  "&itemspage=%d"\
                  "&screenshotspage=%d"\
                  "&videospage=%d"\
                  "&artpage=%d"\
                  "&allguidepage=%d"\
                  "&webguidepage=%d"\
                  "&integratedguidepage=%d"\
                  "&discussionspage=%d"\
                  "&numperpage=10"\
                  "&browsefilter=toprated"\
                  "&browsefilter=toprated"\
                  "&appid=%s"\
                  "&appHubSubSection=10"\
                  "&appHubSubSection=10"\
                  "&l=schinese&filterLanguage=default&searchText=&forceanon=1" % ((page-1)*10, page, page, page, page, page, page, page, page, page, page, page, page, appid))
        return suffix

    def remove_html(self, html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', html)
        return cleantext


    def seek_args(self, string, ids):
        res = []
        pos_s3 = 0
        while pos_s3 >= 0 :
            pos_p = string.find("<div class=\"date_posted\">", pos_s3)
            if pos_p > 0:
                pos_s2 = string.find("</div>", pos_p)
                pos_s3 = string.find("</div>", pos_s2+6)
                review = string[pos_s2+6:pos_s3].strip()
                review = self.remove_html(review)
                self.db.update_review(ids, review)
            else:
                break
            res.append(review)
        return res

    def get_review(self, ids):
        res_all = []
        for i in range(1, 20):
            try:
                url = base_url + ids + self.make_suffix(ids, i)
                print(url)
                r = urllib2.urlopen(url)
                res_a = self.seek_args(r.read(), ids)
                for a in res_a:
                    res_all.append(a)
            except Exception, e:
                print(e)
        return res_all
