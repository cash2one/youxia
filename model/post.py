#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 mifan.tv

from lib.query import Query

class PostModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "post"
        super(PostModel, self).__init__()

    def add_new_post(self, post_info):
        return self.data(post_info).add()

    def get_post_by_post_id(self, post_id):
        where = "post.id = %s" % post_id
        field = "post.*"
        return self.where(where).field(field).find()

    def get_post_by_post_id_with_user(self, post_id, user_id):
        where = "post.id = %s" % post_id
        join = "LEFT JOIN ylike ON 'to_post' = ylike.like_type AND post.id = ylike.like_to AND ylike.author_id = %s" % user_id
        field = "post.*, \
                ylike.id as like_id"
        return self.where(where).join(join).field(field).find()

    def update_post_by_post_id(self, post_id, post_info):
        where = "post.id = %s" % post_id
        return self.where(where).data(post_info).save()

    def delete_post_by_post_id(self, post_id):
        where = "post.id = %s" % post_id
        return self.where(where).delete()

    def get_all_posts(self, num = 20, current_page = 1):
        order = "post.id DESC"
        field = "post.*"
        return self.order(order).field(field).pages(current_page = current_page, list_rows = num) 

    def get_user_all_posts(self, user_name, num = 20, current_page = 1):
        where = "post.author_username = '%s'" % user_name
        order = "post.id DESC"
        field = "post.*"
        return self.where(where).order(order).field(field).pages(current_page = current_page, list_rows = num) 

    def get_user_all_posts_with_user(self, user_name, user_id, num = 20, current_page = 1):
        where = "post.author_username = '%s'" % user_name
        join = "LEFT JOIN ylike ON 'to_post' = ylike.like_type AND post.id = ylike.like_to AND ylike.author_id = %s" % user_id
        order = "post.id DESC"
        field = "post.*, \
                ylike.id as like_id"
        return self.where(where).join(join).order(order).field(field).pages(current_page = current_page, list_rows = num) 