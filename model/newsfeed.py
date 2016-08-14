#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 mifan.tv

from lib.query import Query

class NewsfeedModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "newsfeed"
        super(NewsfeedModel, self).__init__()

    def add_new_newsfeed(self, newsfeed_info):
        return self.data(newsfeed_info).add()

    def get_newsfeed_by_id(self, newsfeed_id):
        where = "newsfeed.id = '%s'" % newsfeed_id
        return self.where(where).find()

    def update_newsfeed_by_id(self, newsfeed_id, newsfeed_info):
        where = "newsfeed.id = %s" % newsfeed_id
        return self.where(where).data(newsfeed_info).save()

    def get_all_newsfeeds(self, num = 10, current_page = 1):
        order = "newsfeed.id DESC"
        field = "newsfeed.*"
        return self.order(order).field(field).pages(current_page = current_page, list_rows = num) 

    def get_all_newsfeeds_count(self):
        return self.count()

    def delete_newsfeed_by_id(self, newsfeed_id):
        where = "newsfeed.id = %s " % newsfeed_id
        return self.where(where).delete()