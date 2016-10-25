#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 mifan.tv

from lib.query import Query

class ColorModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "color"
        super(ColorModel, self).__init__()

    def add_new_color(self, color_info):
        return self.data(color_info).add()

    def get_color_by_id(self, color_id):
        where = "color.id = '%s'" % color_id
        return self.where(where).find()

    def get_rand_color(self):
        order = "RAND()"
        limit = "1"
        return self.order(order).limit(limit).select()