#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 mifan.tv

from lib.query import Query

class ItemModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "item"
        super(ItemModel, self).__init__()

    def add_new_item(self, item_info):
        return self.data(item_info).add()

    def get_item_by_id(self, item_id):
        where = "item.id = '%s'" % item_id
        return self.where(where).find()

    

    def get_like_by_author_and_item_id(self, author_id, item_id):
        where = "item.author_id = %s AND item.id = %s AND item.first_type='like'" % (author_id, item_id)
        return self.where(where).find()
        

    def update_item_by_id(self, item_id, item_info):
        where = "item.id = %s" % item_id
        return self.where(where).data(item_info).save()

    def get_all_items(self, num = 10, current_page = 1):
        order = "item.id DESC"
        field = "item.*"
        return self.order(order).field(field).pages(current_page = current_page, list_rows = num) 

    def get_all_items_count(self):
        return self.count()

    def get_max_post_id(self, field="post_id"):
        return self.max(field)

    def delete_item_by_id(self, item_id):
        where = "item.id = %s " % item_id
        return self.where(where).delete()

    

    