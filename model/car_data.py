#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 meiritugua.com

import time
from lib.query import Query

class Car_dataModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "car_data"
        super(Car_dataModel, self).__init__()

    def add_new_car_data(self, car_data_info):
        return self.data(car_data_info).add()

    def get_all_car_brands(self, num = 10, current_page = 1):
    	where = "car_data.data_type = 'brand'"
        order = "car_data.id DESC"
        field = "car_data.*"
        return self.order(order).field(field).pages(current_page = current_page, list_rows = num) 

    def get_all_car_venders(self, num = 10, current_page = 1):
    	where = "car_data.data_type = 'vender'"
        order = "car_data.id DESC"
        field = "car_data.*"
        return self.order(order).field(field).pages(current_page = current_page, list_rows = num) 

    def get_all_car_models(self, num = 10, current_page = 1):
    	where = "car_data.data_type = 'model'"
        order = "car_data.id DESC"
        field = "car_data.*"
        return self.order(order).field(field).pages(current_page = current_page, list_rows = num) 
