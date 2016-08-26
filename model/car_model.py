#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2013 meiritugua.com

import time
from lib.query import Query

class Car_modelModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "car_model"
        super(Car_modelModel, self).__init__()

    def add_new_car_model(self, car_model_info):
        return self.data(car_model_info).add()