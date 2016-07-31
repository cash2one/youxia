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

access_key = "8RGFv3IumZByltTM1dxc9ZMAeij78rvTkjDd6WLs"
secret_key = "Ge61JJtUSC5myXVrntdVOqAZ5L7WpXR_Taa9C8vb"
q = Auth(access_key, secret_key)
bucket = BucketManager(q)


class IndexHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        
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
            

class IndexAdminHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["side_menu"] = "dashboard"
        template_variables["user_info"] = user_info
        template_variables["user_count"] = 0
        template_variables["course_count"] = 0
        if(user_info and (user_info.admin == "admin" or user_info.admin == "teacher")):  
            self.render("admin/index.html", **template_variables)
        else:
            self.render("admin/index.html", **template_variables)

class CoursesAdminHandler(BaseHandler):
    def get(self, template_variables = {}):
        template_variables["side_menu"] = "courses"
        user_info = self.current_user
        template_variables["user_info"] = user_info
        p = int(self.get_argument("p", "1"))

        if(user_info):
            if(user_info.admin == "admin"):  
                template_variables["all_courses"] = 0
            if(user_info.admin == "teacher"):
                template_variables["all_courses"] = 0
            self.render("admin/courses.html", **template_variables)
        else:
            self.render("admin/courses.html", **template_variables)