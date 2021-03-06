#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2016 youxia

import uuid
import hashlib
from PIL import Image
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
from lib.dateencoder import DateEncoder
from lib.utils import getJsonKeyValue

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
        template_variables["page_name"] = "App--index"

        page = int(self.get_argument("page", "1"))

        all_posts = self.post_model.get_all_posts(current_page = page)
        template_variables["all_posts"] = all_posts
        
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

class ReviewsHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        p = int(self.get_argument("p", "1"))

        all_cars1 = self.car_data_model.get_car_models_by_sort("热门车", current_page = p)
        template_variables["all_cars1"] = all_cars1
       
        self.render(self.template_path+"review.html", **template_variables)

class BbsHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        p = int(self.get_argument("p", "1"))
       
        self.render(self.template_path+"bbs.html", **template_variables)

class TagHandler(BaseHandler):
    def get(self, tag_name, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        p = int(self.get_argument("p", "1"))

        tag = self.tag_model.get_tag_by_tag_name(tag_name)
        template_variables["tag"] = tag
       
        self.render(self.template_path+"tag.html", **template_variables)

class PostHandler(BaseHandler):
    def get(self, post_id, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        p = int(self.get_argument("p", "1"))
        template_variables["page_name"] = "App--discussion"

        if user_info:
            post = self.post_model.get_post_by_post_id_with_user(post_id, user_info.uid)
        else:
            post = self.post_model.get_post_by_post_id(post_id)
        template_variables["post"] = post
        #template_variables["tags"] = self.post_tag_model.get_post_all_tags(post_id)

        self.render(self.template_path+"post.html", **template_variables)

class NewHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        self.render(self.template_path+"new.html", **template_variables)

    @tornado.web.authenticated
    def post(self, template_variables = {}):
        user_info = self.current_user
        template_variables = {}

        post_type = self.get_argument('action', "save")

        post_info = {}
        data = json.loads(self.request.body)

        post_info = getJsonKeyValue(data, post_info, "title")
        post_info = getJsonKeyValue(data, post_info, "content")
        post_info = getJsonKeyValue(data, post_info, "board")
        post_info = getJsonKeyValue(data, post_info, "models")

        post_info["author_id"] = user_info["uid"]
        post_info["author_username"] = user_info["username"]
        if user_info["avatar"]:
            post_info["author_avatar"] = user_info["avatar"]
        if user_info["color"]:
            post_info["author_color"] = user_info["color"]
        post_info["updated"] = time.strftime('%Y-%m-%d %H:%M:%S')
        post_info["created"] = time.strftime('%Y-%m-%d %H:%M:%S')

        post_id = self.post_model.add_new_post(post_info)
        if post_id:
            success = 0
            message = "成功新建帖子"
            redirect = "/post/"+str(post_id)
        else:
            success = -1
            message = "新建帖子失败"
            redirect = ""

        self.write(lib.jsonp.print_JSON({
            "success": success,
            "message": message,
            "redirect": redirect
        }))

        board_tag = self.tag_model.get_tag_by_tag_name(post_info["board"])
        if board_tag:
            self.post_tag_model.add_new_post_tag({"post_id": post_id, "tag_id": board_tag.id})
            self.tag_model.update_tag_by_tag_id(board_tag.id, {"post_num": board_tag.post_num+1})

        models_tag = self.tag_model.get_tag_by_tag_name(post_info["models"])
        if models_tag:
            self.post_tag_model.add_new_post_tag({"post_id": post_id, "tag_id": models_tag.id})
            self.tag_model.update_tag_by_tag_id(models_tag.id, {"post_num": models_tag.post_num+1})


        '''
        # process tags
        tagStr = data["tags"]
        print tagStr
        if tagStr:
            tagNames = tagStr.split(',') 
            for tagName in tagNames:  
                tag = self.tag_model.get_tag_by_tag_name(tagName)
                if tag:
                    self.post_tag_model.add_new_post_tag({"post_id": post_id, "tag_id": tag.id})
                    self.tag_model.update_tag_by_tag_id(tag.id, {"post_num": tag.post_num+1})
        '''

        


class UploadImageHandler(BaseHandler):
    def post(self, template_variables = {}):
        template_variables = {}
        # validate the fields
        if("files" in self.request.files):            
            file_name = "%s" % uuid.uuid1()
            file_raw = self.request.files["files"][0]["body"]
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

            self.write(lib.jsonp.print_JSON({
                    "files": [
                        {
                            "name": file_name,
                        }]
            }))
class ReplyHandler(BaseHandler):
    def get(self, post_id, template_variables = {}):
        print 'fdsafsadf'
        user_info = self.current_user
        page = int(self.get_argument("page", "1"))

        if user_info:
            all_replys = self.reply_model.get_post_all_replys_with_user_sort_by_created(post_id, user_info.uid, current_page = page)
        else:
            all_replys = self.reply_model.get_post_all_replys_sort_by_created(post_id, current_page = page)
        
        '''
        print 'cccccc@@@@@@@@@@@@@@@@@@@'
        print all_replys
        print 'ddddd'
        for reply in all_replys['list']:
            reply['reply_replys'] = self.reply_model.get_reply_all_replys_sort_by_created(reply.id)
        print 'eeeee'
        '''
        replys_json = json.dumps(all_replys, cls=DateEncoder)
        print replys_json
        self.write(replys_json)

    @tornado.web.authenticated
    def post(self, post_id, template_variables = {}):
        user_info = self.current_user

        data = json.loads(self.request.body)
        content = data["content"]
        reply_type = data["reply_type"]
        reply_to = data["reply_to"]

        if(user_info):
            # update post
            post = self.post_model.get_post_by_post_id(post_id)
            self.post_model.update_post_by_post_id(post.id, {
                "reply_num": post.reply_num+1, 
                "last_reply_user": user_info.username,
                "last_reply_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "updated": time.strftime('%Y-%m-%d %H:%M:%S'),
            })

            # update reply_item
            if (reply_type == 'to_reply'):
                reply = self.reply_model.get_reply_by_id(reply_to)
                self.reply_model.update_reply_by_id(reply.id, {
                    "reply_num": reply.reply_num+1,
                    "reply_users": reply.reply_users if reply.reply_users else '' + user_info.username + ',',
                    "updated": time.strftime('%Y-%m-%d %H:%M:%S'),
                })


            reply_info = {
                "author_id": user_info["uid"],
                "author_username": user_info["username"],
                "post_id": post_id,
                "content": content,
                "reply_type": reply_type,
                "reply_to": reply_to,
                "created": time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            if user_info["avatar"]:
                reply_info["author_avatar"] = user_info["avatar"]
            if user_info["color"]:
                reply_info["author_color"] = user_info["color"]
            reply_id = self.reply_model.add_new_reply(reply_info)
            reply_info["id"] = reply_id
            self.write(lib.jsonp.print_JSON({
                    "success": 1,
                    "message": "successed",
                    "reply_info": reply_info
            }))
        else:
            self.write(lib.jsonp.print_JSON({
                    "success": 0,
                    "message": "failed",
            }))

class LikeHandler(BaseHandler):
    def get(self, like_to, template_variables = {}):
        user_info = self.current_user

        like_type = self.get_argument("like_type", "to_reply")

        if(user_info):
            if (like_type == "to_post"):
                like = self.ylike_model.get_like_by_user_and_post(user_info.uid, like_to)
            else:
                like = self.ylike_model.get_like_by_user_and_reply(user_info.uid, like_to)
            if not like:
                if (like_type == "to_post"):
                    post = self.post_model.get_post_by_post_id(like_to)
                    self.post_model.update_post_by_post_id(like_to, {
                        "like_num": post.like_num+1,
                        "like_users": post.like_users if post.like_users else '' + user_info.username + ','
                    })
                else:
                    reply = self.reply_model.get_reply_by_id(like_to)
                    self.reply_model.update_reply_by_id(like_to, {
                        "like_num": reply.like_num+1,
                        "like_users": reply.like_users if reply.like_users else '' + user_info.username + ','
                    })
                
                self.ylike_model.add_new_like({
                    "like_type": like_type,
                    "like_to": like_to,
                    "author_id": user_info.uid,
                    "created": time.strftime('%Y-%m-%d %H:%M:%S')
                })
                
            self.write(lib.jsonp.print_JSON({
                    "success": 1,
                    "message": "successed",
                }))
        else:
            self.write(lib.jsonp.print_JSON({
                    "success": 0,
                    "message": "successed",
                }))

class TagsHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        template_variables["static_path"] = self.static_path
        template_variables["user_info"] = user_info
        p = int(self.get_argument("p", "1"))
       
        self.render(self.template_path+"tags.html", **template_variables)