#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2016 youxia

import uuid
import hashlib
import Image
import StringIO
import time
import json
import re
import urllib2
import tornado.web
import lib.jsonp
import pprint
import math
import datetime
import os
import requests
import MySQLdb
import helper

from base import *
from lib.sendmail import send
from lib.variables import *
from lib.variables import gen_random
from lib.xss import XssCleaner
from lib.utils import find_mentions
from lib.reddit import hot
from lib.utils import pretty_date
from pyquery import PyQuery as pyq
from lib.dateencoder import DateEncoder

from lib.mobile import is_mobile_browser
from lib.mobile import is_weixin_browser

from qiniu import Auth
from qiniu import BucketManager
from qiniu import put_data

import xml.etree.ElementTree as ET
import commands

access_key = "FyIIPvo4crjBvyQas_Y50Nsob1Yz3QUZuKCTgru8"
secret_key = "RUeH0GpomE2vymovye58aevY9_FrGhbfpcGWWsQI"
q = Auth(access_key, secret_key)
bucket = BucketManager(q)


class IndexHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info

        p = int(self.get_argument("p", "1"))
        all_nowfeeds = self.nowfeed_model.get_all_nowfeeds(current_page = p)
        template_variables["all_nowfeeds"] = all_nowfeeds

        if(user_info):
            print 'ddd'
        else:
            print 'dasfafafasd'
            template_variables["sign_in_up"] = self.get_argument("s", "") 
            link = self.get_argument("link", "")
            if link!="":
                template_variables["link"] =  link
            link2 = self.get_argument("link2", "")
            if link2!="":
                template_variables["link2"] = link2 
            invite = self.get_argument("i", "")
            if invite!="":
                template_variables["invite"] = invite
            else:
                template_variables["invite"] = None
            error = self.get_argument("e", "")
            if error!="":
                template_variables["error"] = error
            else:
                template_variables["error"] = None
        self.render(self.template_path+"index.html", **template_variables)

class PostHandler(BaseHandler):
    def get(self, post_id, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        self.render(self.template_path+"post.html", **template_variables)

class NewHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        self.render(self.template_path+"new.html", **template_variables)

class UploadImageHandler(BaseHandler):
    def post(self, template_variables = {}):
        template_variables = {}
        # validate the fields
        if("files[]" in self.request.files):            
            file_name = "%s" % uuid.uuid1()
            file_raw = self.request.files["files[]"][0]["body"]
            file_buffer = StringIO.StringIO(file_raw)
            file = Image.open(file_buffer)

            usr_home = os.path.expanduser('~')
            file.save(usr_home+"/%s.png" % file_name, "PNG")  

            uptoken = q.upload_token("yx-img", "%s.png" % file_name)
            data=open(usr_home+"/%s.png" % file_name)
            ret, info = put_data(uptoken, "%s.png" % file_name, data)
 
            os.remove(usr_home+"/%s.png" % file_name)

            file_name = "http://objdsnsh2.bkt.clouddn.com/"+file_name+".png"
            print file_name

            self.write(file_name)
