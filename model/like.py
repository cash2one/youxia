#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 mifan.tv

from lib.query import Query

class LikeModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "like"
        super(LikeModel, self).__init__()

    def get_like_by_user_and_reply(self, author_id, reply_id):
        where = "author_id = %s AND reply_id = %s" % (author_id, reply_id)
        return self.where(where).find()

    def get_like_by_user_and_post(self, author_id, post_id):
        where = "author_id = %s AND post_id = %s" % (author_id, post_id)
        return self.where(where).find()

    def delete_like_by_id(self, like_id):
        where = "like.id = %s " % like_id
        return self.where(where).delete()

    def delete_like_by_reply_id(self, reply_id):
        where = "like.reply_id = %s " % reply_id
        return self.where(where).delete()

    def update_like_by_id(self, like_id, like_info):
        where = "like.id = %s" % like_id
        return self.where(where).data(like_info).save()

    def add_new_like(self, like_info):
        return self.data(like_info).add()

    def get_reply_all_likes(self, reply_id, num = 3, current_page = 1):
        where = "like.reply_id = %s" % reply_id
        join = "LEFT JOIN user ON like.author_id = user.uid"
        order = "like.created DESC, like.id DESC"
        field = "like.*, \
                user.username as author_username, \
                user.avatar as author_avatar"
        return self.where(where).order(order).join(join).field(field).pages(current_page = current_page, list_rows = num)

