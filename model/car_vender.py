#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 meiritugua.com

import time
from lib.query import Query

class Car_venderModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "car_vender"
        super(Car_venderModel, self).__init__()

    def add_new_car_vender(self, car_vender_info):
        return self.data(car_vender_info).add()