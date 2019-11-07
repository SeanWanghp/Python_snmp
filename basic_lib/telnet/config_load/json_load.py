
# -*- coding:utf-8 -*-
# C:\Python37\
__author__ = 'Sean Wang'
#data@:2019-10-22
#update data@:2019-xx-xx                  #spell inspection cancelled
import json
from collections import OrderedDict


class jon_load:

    def __init__(self, json_da=None):
        value = {}
        self.df = None
        self.lf = None
        json_data = {'status': 'success', 'code': 200,
                        'data': {'username': 'bob', 'user_level': 6, 'nickname': 'playboy'}}
        if self.df is None:
            self.df = b'config.json'
        if self.lf is None:
            self.lf = b'config.json'
        self.dump_json(self.df, json_data)
        self.load_json(self.lf)

    def dump_json(self, df, json_data):
        with open(df, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)

    def load_json(self, lf):
        with open(lf, 'r', encoding='utf-8') as f:
            # ff = json.loads(f, object_pairs_hook=OrderedDict)
            ff = json.load(f)
            print('json data: ', ff)
            print(ff.keys(), ff.values())

# jon_load()

