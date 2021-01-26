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
        self.mksqlite()
        self.read_input()
# }}}
    def read_input(self):# {{{
        self.scenariusze=self.json.read('input.json')
        for i in self.scenariusze:
            self.eval_scenariusz(i)
# }}}
    def mksqlite(self):# {{{
        if os.path.exists("db.sqlite"):
            os.remove("db.sqlite")
        self.s=Sqlite("db.sqlite")
        self.s.query("create table czynnosci(wewn,dym,pion_schody,pion_dzwig,wartosc,czynnosc)")
        data=[]

        #              wewn , dym , pion_schody , pion_dzwig , wartosc , czynnosc
        data.append([ 0     , 0   , 0           , 0          , 50      , 't.przygotowania']) ,
        data.append([ 0     , 0   , 0           , 0          , 1       , 'v.poziom'       ]) ,
        data.append([ 1     , 0   , 0           , 0          , 0.8     , 'v.poziom'       ]) ,
        data.append([ 1     , 1   , 0           , 0          , 0.36    , 'v.poziom'       ]) ,
        data.append([ 1     , 0   , 1           , 0          , 100     , 't.pion.12m'     ]) ,
        data.append([ 1     , 1   , 1           , 0          , 140     , 't.pion.12m'     ]) ,
        data.append([ 1     , 0   , 1           , 0          , 330     , 't.pion.25m'     ]) ,
        data.append([ 1     , 1   , 1           , 0          , 500     , 't.pion.25'      ]) ,

        self.s.executemany('insert into czynnosci values ({})'.format(','.join('?' * len(data[0]))), data)
# }}}
    def eval_droga(self,d):# {{{
        params={}
        dd(d)
        params['wewn']=1 if d['opis'][0]==1 else 0
        dd(params)
        exit()

        val=d.s.query("select wartosc from czynnosci where czynnosc=? and wewn=? and dym=?", ('v.poziom', 1, 0))[0]['wartosc']
        dd(d)
        exit()
# }}}
    def eval_scenariusz(self, i):# {{{
        for d in i['droga']:
            self.eval_droga(d)
        val=d.s.query("select wartosc from czynnosci where czynnosc=? and wewn=? and dym=?", ('v.poziom', 1, 0))[0]['wartosc']
        print(val)
# }}}

d=DojazdMW()
