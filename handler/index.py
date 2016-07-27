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
        template_variables["static_path"] = self.static_path
        self.render(self.template_path+"index.html", **template_variables)