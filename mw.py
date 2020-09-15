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
        f=self.json.read(sys.argv[1])
        dd(f['fire'])
        dd(len(f['vehicles']))
# }}}

DojazdMW()
