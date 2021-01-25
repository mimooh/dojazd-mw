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
        if os.path.exists("db.sqlite"):
            os.remove("db.sqlite")
        self.s=Sqlite("db.sqlite")
        self.s.query("create table rozwiniecia(rozwiniecie,opis,czas,osob)")
        data=[]
        data.append(['r1', 'jakiś opis', 120, 2 ]),
        data.append(['r2', 'jakiś opis', 130, 2 ]),
        data.append(['r3', 'jakiś opis', 140, 2 ]),

        self.s.executemany('insert into rozwiniecia values ({})'.format(','.join('?' * len(data[0]))), data)
        dd(self.s.query("select * from rozwiniecia where czas < 130"))
# }}}

# czynnosc        ; poziom ; wewn ; dym ; wartosc
# t.przygotowania ;        ; 0    ; 0   ; 50
# v.poziom        ; 1      ; 0    ; 0   ; 1
# v.poziom        ; 1      ; 1    ; 0   ; 0.8
# v.poziom        ; 1      ; 1    ; 1   ; 0.36
# t.pion.12m      ; 0      ; 1    ; 0   ; 100
# t.pion.12m      ; 0      ; 1    ; 1   ; 140
# t.pion.25m      ; 0      ; 1    ; 0   ; 330
# t.pion.25       ; 0      ; 1    ; 1   ; 500


DojazdMW()
