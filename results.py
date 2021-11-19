import json
import os
import sys
import svgwrite
from collections import OrderedDict
from numpy.random import uniform
from include import Json
from include import Dump as dd
from include import Segments_maps

class DojazdMWResults:

    def __init__(self):# {{{
        if len(sys.argv) < 2:
            self.zbior='symulacje/office123/sesja1'
        else:
            self.zbior=sys.argv[1]
        self.json=Json()
        self.maps=Segments_maps().maps
        self.main()
# }}}
    def make_chunks(self, lst, n):# {{{
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
# }}}
    def ranking_skaluj_samochody(self, gdzie):# {{{
        s=sorted(self.img[gdzie]['best_samochody'])
        cc=int(len(s) / 5)
        if cc < 1:
            print("Potrzeba minimum 5 wyników żeby stworzyć analizę graficzną SVG dla wariantu {}".format(gdzie))
            self.img[gdzie]['samochody']={ (1,1): [ (0, [0,0] ) ] }
        else:
            chunks=list(self.make_chunks(s, cc))
            self.img[gdzie]['samochody']={ (6,6): chunks[0], (4,4): chunks[1], (3,3): chunks[2], (2,2):chunks[3], (1,1): chunks[4] }
# }}}
    def make_stats(self):# {{{
        ''' Statystyka: ten byl najlepszy 100 razy, a ten 20 razy '''

        count={}
        for i in self.stats:
            if self.maps['wariants'][i[0]] not in count:
                count[self.maps['wariants'][i[0]]]=0
            count[self.maps['wariants'][i[0]]]+=1
        self.json.write(count, '{}/wyniki_stats.json'.format(self.zbior))
# }}}
    def read_wyniki(self):# {{{
        ''' bit8=0: wariant wewnętrzny '''

        with open('{}/wyniki.txt'.format(self.zbior)) as f: 
            x=f.readlines()
        zewn=[]
        wewn=[]
        self.stats=[]
        self.img={ 'zewn': { 'best_samochody': [] } , 'wewn': { 'best_samochody': [] } , 'pozary': [] }
        for i in x:
            ii=json.loads(i)
            if ii['results']['best']['wariant'][-9] == '0':
                wewn.append(ii)
            else:
                zewn.append(ii)

        self.img['obrys']=self.json.read('{}/conf.txt'.format(self.zbior))['conf']['ogolne']['obrys_budynku']
        for i in zewn:
            if i['results']['best']['wariant'] != None:
                self.img['zewn']['best_samochody'].append((i['results']['best']['czas'], i['xy_samochody']))
                self.img['pozary'].append(i['xyz_pozar'])
                self.stats.append((i['results']['best']['wariant'], i['results']['best']['czas']))
        for i in wewn:
            if i['results']['best']['wariant'] != None:
                self.img['wewn']['best_samochody'].append((i['results']['best']['czas'], i['xy_samochody']))
                self.img['pozary'].append(i['xyz_pozar'])
                self.stats.append((i['results']['best']['wariant'], i['results']['best']['czas']))
# }}}
    def svgwrite(self, gdzie):# {{{
        dwg = svgwrite.Drawing('{}/best_{}.svg'.format(self.zbior, gdzie), profile='tiny')
        dwg.add(dwg.polyline(self.img['obrys'], fill='#fff', stroke_width=0.3, stroke='blue'))
        for i in self.img['pozary']:
            randx=i[0] + uniform(-2,2)
            randy=i[1] + uniform(-2,2)
            dwg.add(dwg.ellipse(center=(randx,randy), r=(1, 1), fill='#f00', opacity=0.3, stroke_width=0.2, stroke='#c00'))
        for i,pozycje in self.img[gdzie]['samochody'].items():
            for p in pozycje:
                randx=p[1][0] + uniform(-3,3)
                randy=p[1][1] + uniform(-3,3)
                dwg.add(dwg.ellipse(center=(randx,randy), opacity=0.2, fill='#aaa', r=i, stroke_width=0.1, stroke='#000')) 
        dwg.save()
# }}}
    def main(self):# {{{
        self.read_wyniki()
        self.make_stats()
        for gdzie in [ 'zewn', 'wewn' ]:
            self.ranking_skaluj_samochody(gdzie)
            self.svgwrite(gdzie)
            if os.environ['USERNAME']=='mimooh': 
                print("{}/wyniki_stats.json".format(self.zbior))
                os.system('inkscape {} -b white -h 1000 -D -e {} 2>/dev/null 1>/dev/null'.format('{}/best_{}.svg'.format(self.zbior,gdzie), '{}/best_{}.png'.format(self.zbior, gdzie)))
                os.system('feh {}/best_{}.png'.format(self.zbior, gdzie))
# }}}

d=DojazdMWResults()

# symulacje/office123/sesja1/wyniki_stats.json
