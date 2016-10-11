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

    def get_post_by_post_id(self, post_id):
        where = "item.post_id = %s AND item.first_type='post'" % post_id
        join = "LEFT JOIN user AS author_user ON item.author_id = author_user.uid"
        field = "item.*, \
                author_user.username as author_username, \
                author_user.avatar as author_avatar, \
                author_user.sign as author_sign"
        return self.where(where).join(join).field(field).find()

    def get_post_by_post_id_with_user(self, post_id, user_id):
        where = "item.post_id = %s AND item.first_type='post'" % post_id
        join = "LEFT JOIN user AS author_user ON item.author_id = author_user.uid\
                LEFT JOIN item AS like_item ON item.id = like_item.reply_to AND like_item.author_id = %s" % user_id
        field = "item.*, \
                author_user.username as author_username, \
                author_user.avatar as author_avatar,\
                like_item.id as like_id"
        return self.where(where).join(join).field(field).find()

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

    def get_post_all_replys_sort_by_created(self, post_id, num = 100, current_page = 1):
        where = "item.post_id = %s AND item.first_type='reply'" % post_id
        join = "LEFT JOIN user ON item.author_id = user.uid"
        order = "item.created ASC, item.id ASC"
        field = "item.*, \
                user.username as author_username, \
                user.avatar as author_avatar"
        return self.where(where).order(order).join(join).field(field).pages(current_page = current_page, list_rows = num)

    def get_post_all_replys_with_user_sort_by_created(self, post_id, user_id, num = 100, current_page = 1):
        where = "item.post_id = %s AND item.first_type='reply'" % post_id
        join = "LEFT JOIN user ON item.author_id = user.uid\
                LEFT JOIN item AS like_item ON item.id = like_item.reply_to AND like_item.author_id = %s" % user_id
        order = "item.created ASC, item.id ASC"
        field = "item.*, \
                user.username as author_username, \
                user.avatar as author_avatar, \
                like_item.id as like_id"
        return self.where(where).order(order).join(join).field(field).pages(current_page = current_page, list_rows = num)

    def get_all_posts(self, num = 5, current_page = 1):
        where = "item.first_type='post'"
        order = "item.post_id DESC"
        join = "LEFT JOIN user AS author_user ON item.author_id = author_user.uid"
        field = "item.*, \
                author_user.username as author_username, \
                author_user.avatar as author_avatar"
        return self.where(where).order(order).join(join).field(field).pages(current_page = current_page, list_rows = num) 