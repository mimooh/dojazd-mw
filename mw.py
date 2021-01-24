import json
import shutil
import os
import re
import sys
import codecs
import itertools

from collections import OrderedDict
from numpy.random import uniform
from math import sqrt
from math import floor
from include import Sqlite
from include import Json
from include import Dump as dd

class DojazdMW:
    def __init__(self):# {{{
        self.s=Sqlite("mw.sqlite")
        self.json=Json()
        self.read_input()
        self.mksqlite()
# }}}
    def read_input(self):# {{{
        f=self.json.read('input.json')
        for i in f:
            print(i, i['scenariusz'])
# }}}
    def mksqlite(self):# {{{
        self.s.query("drop table rozwiniecia")
        self.s.query("create table rozwiniecia(rozwiniecie,opis,czas,osob)")
        data=[]
        data.append(['r1', 'jakiś opis', 120, 2 ]),
        data.append(['r2', 'jakiś opis', 130, 2 ]),
        data.append(['r3', 'jakiś opis', 140, 2 ]),

        self.s.executemany('insert into rozwiniecia values ({})'.format(','.join('?' * len(data[0]))), data)
        dd(self.s.query("select * from rozwiniecia where czas < 130"))
# }}}

DojazdMW()
