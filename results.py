import json
import sys
from collections import OrderedDict
from include import Json
from include import Dump as dd
import svgwrite

class DojazdMWResults:

    def __init__(self):# {{{
        if len(sys.argv) < 2:
            self.zbior='office123/sesja1'
        else:
            self.zbior=sys.argv[1]
        self.json=Json()
        self.main()
# }}}

    def read_wyniki(self):# {{{
        with open('symulacje/{}/wyniki.txt'.format(self.zbior)) as f: 
            x=f.readlines()
        dat=[]
        self.img={'obrys':None, 'pozary':[], 'samochody':[]}
        for i in x:
            dat.append(json.loads(i))

        self.img['obrys']=dat[0]['conf']['ogólne']['obrys_budynku']
        for i in dat:
            self.img['pozary'].append(i['conf']['pożar']['xyz'])
            self.img['samochody'].append(i['conf']['ogólne']['xy_samochody'])
# }}}
    def svgwrite(self):# {{{
        dd(222)
        dwg = svgwrite.Drawing('symulacje/{}/best.svg'.format(self.zbior), profile='tiny')
        dwg.add(dwg.polyline(self.img['obrys'], fill='#fff', stroke_width=0.2, stroke='blue'))
        for i in self.img['pozary']:
            dwg.add(dwg.ellipse(center=(i[0],i[1]), r=(3, 3), fill='#f40', opacity=0.5))
        for i in self.img['samochody']:
            dwg.add(dwg.rect(insert=(i[0],i[1]), size=(3, 3), fill='#000', opacity=0.1))
        dwg.save()
# }}}
    def main(self):# {{{
        self.read_wyniki()
        self.svgwrite()
# }}}

d=DojazdMWResults()
