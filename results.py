import json
import os
import sys
import svgwrite
from collections import OrderedDict
from include import Json
from include import Dump as dd

class DojazdMWResults:

    def __init__(self):# {{{
        if len(sys.argv) < 2:
            self.zbior='office123/sesja1'
        else:
            self.zbior=sys.argv[1]
        self.json=Json()
        self.main()
# }}}
    def make_chunks(self, lst, n):# {{{
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
# }}}
    def make_ranking(self):# {{{
        s=sorted(self.bests)
        cc=int(len(s) / 5)
        if cc < 1:
            print("Potrzeba minimum 5 symulacji")
            exit()
        chunks=list(self.make_chunks(s, cc))
        self.img['samochody']={ (5,5): chunks[0], (4,4): chunks[1], (3,3): chunks[2], (2,2):chunks[3], (1,1): chunks[4] }
# }}}
    def make_stats(self):# {{{
        ''' Statystyka: ten był najlepszy 100 razy, a ten 20 razy '''

        count={}
        for i in self.stats:
            if i[0] not in count:
                count[i[0]]=0
            count[i[0]]+=1
        self.json.write(count, 'symulacje/{}/wyniki_stats.json'.format(self.zbior))
        if os.environ['USERNAME']=='mimooh': # temp
            print('symulacje/{}/wyniki_stats.json'.format(self.zbior))
# }}}
    def read_wyniki(self):# {{{
        with open('symulacje/{}/wyniki.txt'.format(self.zbior)) as f: 
            x=f.readlines()
        dat=[]
        self.stats=[]
        self.bests=[]
        self.img={'pozary':[], 'samochody':[]}
        for i in x:
            dat.append(json.loads(i))

        self.img['obrys']=self.json.read('symulacje/{}/conf.txt'.format(self.zbior))['conf']['ogólne']['obrys_budynku']
        for i in dat:
            self.img['pozary'].append(i['xyz_pozar'])
            self.stats.append((i['results']['best']['wariant'], i['results']['best']['czas']))
            self.bests.append((i['results']['best']['czas'], i['xy_samochody']))
# }}}
    def svgwrite(self):# {{{
        dwg = svgwrite.Drawing('symulacje/{}/best.svg'.format(self.zbior), profile='tiny')
        dwg.add(dwg.polyline(self.img['obrys'], fill='#fff', stroke_width=0.3, stroke='blue'))
        for i in self.img['pozary']:
            dwg.add(dwg.ellipse(center=(i[0],i[1]), r=(3, 3), fill='#f40', opacity=0.5))
        for i,pozycje in self.img['samochody'].items():
            for p in pozycje:
                dwg.add(dwg.rect(insert=(p[1][0],p[1][1]), size=i, fill='#000', opacity=0.1))
        dwg.save()
        if os.environ['USERNAME']=='mimoohe': 
            os.system('inkscape {} -b white -h 1000 -D -e {}'.format('symulacje/{}/best.svg'.format(self.zbior), 'symulacje/{}/best.png'.format(self.zbior)))
            os.system('feh symulacje/{}/best.png'.format(self.zbior))
        else:
            os.system('inkscape {} -b white -h 1000 -D -o {}'.format('symulacje/{}/best.svg'.format(self.zbior), 'symulacje/{}/best.png'.format(self.zbior)))


# }}}
    def main(self):# {{{
        self.read_wyniki()
        self.make_stats()
        self.make_ranking()
        self.svgwrite()
# }}}

d=DojazdMWResults()

# symulacje/office123/sesja1/wyniki_stats.json
