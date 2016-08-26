#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 meiritugua.com

import time
from lib.query import Query

class Car_brandModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "car_brand"
        super(Car_brandModel, self).__init__()

    def add_new_car_brand(self, car_brand_info):
        return self.data(car_brand_info).add()