#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 mifan.tv

from lib.query import Query

class YlikeModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "ylike"
        super(YlikeModel, self).__init__()

    def get_like_by_user_and_reply(self, author_id, reply_id):
        where = "author_id = %s AND like_to = %s AND like_type = 'to_reply'" % (author_id, reply_id)
        return self.where(where).find()

    def get_like_by_user_and_post(self, author_id, post_id):
        where = "author_id = %s AND post_id = %s AND like_type = 'to_post'" % (author_id, post_id)
        return self.where(where).find()

    def delete_like_by_id(self, like_id):
        where = "id = %s " % like_id
        return self.where(where).delete()

    def delete_like_by_reply_id(self, reply_id):
        where = "reply_id = %s " % reply_id
        return self.where(where).delete()

    def update_like_by_id(self, like_id, like_info):
        where = "id = %s" % like_id
        return self.where(where).data(like_info).save()

    def add_new_like(self, like_info):
        return self.data(like_info).add()

