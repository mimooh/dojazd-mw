import json
from collections import OrderedDict
from include import Json
from include import Dump as dd
from include import Sqlite

class DojazdMW:

    def __init__(self):# {{{
        self.json=Json()
        self.make_segments_map()
        self.make_db_czynnosci()
        self.s=Sqlite("sqlite/firetrucks.db")
        self.main()
# }}}
    def query(self, param, dlugosc):# {{{
        if isinstance(self.db_czynnosci[param], dict):
            for t in list(self.db_czynnosci[param].keys()):
                if t >= dlugosc:
                    return self.db_czynnosci[param][t]
        else:
            return self.db_czynnosci[param]

# }}}
    def make_db_czynnosci(self):# {{{
        self.db_czynnosci={
            't_zasilenie_samochodu'                                 : OrderedDict([(20,30)]),
            't_zasilenie_instalacji_w75x1'                          : OrderedDict([(20,70)]),
            't_zasilenie_instalacji_w75x2'                          : OrderedDict([(20,100)]),
            't_sprawianie_motopompy_MP81_z_linia_w75'               : OrderedDict([(20,320)]),
            't_sprawianie_motopompy_szlam_z_linia_w75'              : OrderedDict([(20,510)]),
            't_sprawianie_zbiornika_2i5m3'                          : 290,
            't_sprawianie_zbiornika_5m3'                            : 150,
            't_linia_główna_w75_do_rozdzielacza'                    : 30,
            't_linia_główna_w75x2_do_rozdzielacza_harmonijka'       : 15,
            't_przygotowanie_roty_gaśn'                             : 50,
            'v_rota_gaśn_zewn_poziom_dym0'                          : 1,
            'v_rota_gaśn_wewn_poziom_dym0'                          : 0.8,
            'v_rota_gaśn_wewn_poziom_dym1'                          : 0.38,
            't_rota_gaśn_wewn_pion_dym0'                            : OrderedDict([(12,100),(25,330),(55,1026)]),
            't_rota_gaśn_wewn_pion_dym1'                            : OrderedDict([(12,140),(25,500),(55,1520)]),
            'v_linia_gaśn_w52_wewn_poziom_dym1_kregi'               : 0.25,
            't_linia_gaśn_w52_wewn_pion_dym1_kregi_1rota'           : OrderedDict([(12,620),(25,1120),(55,2120)]),
            't_linia_gaśn_w52_wewn_pion_dym1_kregi_2roty'           : OrderedDict([(12,500),(25,1060),(55,1520)]),
            'v_linia_gaśn_w52_wewn_poziom_dym0_kregi'               : 0.8,
            't_linia_gaśn_w52_wewn_pion_dym0_kregi_1rota'           : OrderedDict([(12,230),(25,760),(55,1700)]),
            't_linia_gaśn_w52_wewn_pion_dym0_kregi_2roty'           : OrderedDict([(12,170),(25,700),(55,1520)]),
            'v_linia_gaśn_w42_wewn_poziom_dym1_kregi'               : 0.26,
            't_linia_gaśn_w42_wewn_pion_dym1_kregi_1rota'           : OrderedDict([(12,620),(25,1120),(55,2120)]),
            't_linia_gaśn_w42_wewn_pion_dym1_kregi_2roty'           : OrderedDict([(12,500),(25,1060),(55,1520)]),
            'v_linia_gaśn_w42_wewn_poziom_dym0_kregi'               : 1,
            't_linia_gaśn_w42_wewn_pion_dym0_kregi_1rota'           : OrderedDict([(12,230),(25,760),(55,1700)]),
            't_linia_gaśn_w42_wewn_pion_dym0_kregi_2roty'           : OrderedDict([(12,170),(25,700),(55,1520)]),
            'v_linia_gaśn_w52_wewn_poziom_dym1_kasetony'            : 0.4,
            't_linia_gaśn_w52_wewn_pion_dym1_kasetony_1rota'        : OrderedDict([(12,560),(25,1000),(55,1940)]),
            't_linia_gaśn_w52_wewn_pion_dym1_kasetony_2roty'        : OrderedDict([(12,320),(25,880),(55,1510)]),
            'v_linia_gaśn_w52_wewn_poziom_dym0_kasetony'            : 1,
            't_linia_gaśn_w52_wewn_pion_dym0_kasetony_1rota'        : OrderedDict([(12,500),(25,940),(55,1880)]),
            't_linia_gaśn_w52_wewn_pion_dym0_kasetony_2roty'        : OrderedDict([(12,320),(25,700),(55,1510)]),
            'v_linia_gaśn_w42_wewn_poziom_dym1_kasetony'            : 0.4,
            't_linia_gaśn_w42_wewn_pion_dym1_kasetony_1rota'        : OrderedDict([(12,500),(25,940),(55,1940)]),
            't_linia_gaśn_w42_wewn_pion_dym1_kasetony_2roty'        : OrderedDict([(12,320),(25,880),(55,1510)]),
            'v_linia_gaśn_w42_wewn_poziom_dym0_kasetony'            : 1.33,
            't_linia_gaśn_w42_wewn_pion_dym0_kasetony_1rota'        : OrderedDict([(12,500),(25,940),(55,1880)]),
            't_linia_gaśn_w42_wewn_pion_dym0_kasetony_2roty'        : OrderedDict([(12,320),(25,700),(55,1510)]),
            't_linia_gaśn_w52_wewn_pion_dym1_dusza_klatki_2roty'    : OrderedDict([(12,500),(25,940),(55,1940)]),
            't_linia_gaśn_w52_wewn_pion_dym1_dusza_klatki_3roty'    : OrderedDict([(12,320),(25,880),(55,1510)]),
            't_linia_gaśn_w52_wewn_pion_dym0_dusza_klatki_2roty'    : OrderedDict([(12,500),(25,940),(55,1880)]),
            't_linia_gaśn_w52_wewn_pion_dym0_dusza_klatki_3roty'    : OrderedDict([(12,320),(25,700),(55,1510)]),
            't_linia_gaśn_w42_wewn_pion_dym1_dusza_klatki_2roty'    : OrderedDict([(12,500),(25,940),(55,1940)]),
            't_linia_gaśn_w42_wewn_pion_dym1_dusza_klatki_3roty'    : OrderedDict([(12,320),(25,880),(55,1510)]),
            't_linia_gaśn_w42_wewn_pion_dym0_dusza_klatki_2roty'    : OrderedDict([(12,440),(25,940),(55,1880)]),
            't_linia_gaśn_w42_wewn_pion_dym0_dusza_klatki_3roty'    : OrderedDict([(12,320),(25,700),(55,1510)]),
            't_szybkie_natarcie_zewn_poziom'                        : OrderedDict([(20,50)]),
            't_szybkie_natarcie_zewn_pion_elewacja'                 : OrderedDict([(12,190)]),
            't_linia_gaśn_w52_elewacja'                             : OrderedDict([(12,440),(25,880),(55,2120)]),
            't_linia_gaśn_w42_elewacja'                             : OrderedDict([(12,430),(25,860),(55,1880)]),
            't_przygotowanie_działań_drabina_dw10'                  : OrderedDict([(20,260)]),
            't_wejście_oknem_drabina_dw10'                          : OrderedDict([(20,230)]),
            't_przygotowanie_działań_drabina_nasadkowa'             : OrderedDict([(20,280)]),
            't_wejście_oknem_drabina_nasadkowa'                     : OrderedDict([(20,250)]),
            't_przygotowanie_działań_drabina_mechaniczna'           : OrderedDict([(12,160), (25,180), (55,400)]),
            't_przygotowanie_działań_podnośnik'                     : OrderedDict([(12,250), (25,290), (55,490)]),
            't_przygotowanie_sprzęt_wentylacja'                     : OrderedDict([(20,120)]),
            't_przygotowanie_roty_gotowość'                         : 25,
            't_przygotowanie_medyczne'                              : 70,
            't_przygotowanie_monitorowania_aparatów_powietrznych'   : 30,
            't_zabezpieczenie_pachołkami'                           : 170,
            't_rozpoznanie_wstepne_3600'                            : 70,
            't_przygotowanie_asekuracji_drabina_dw10'               : OrderedDict([(20,210)]),
            't_przygotowanie_asekuracji_drabina_nasadkowa'          : OrderedDict([(20,230)]),
            't_przygotowanie_asekuracji_drabina_mechaniczna'        : OrderedDict([(12,140), (25,160), (55,380)]),
            't_przygotowanie_asekuracji_podnośnik'                  : OrderedDict([(12,230), (25,260), (55,460)]),
            't_przygotowanie_skokochronu'                           : OrderedDict([(20,130)]),
            't_przygotowanie_asekuracji_rota_RIT'                   : 110,
            't_dotarcie_roty_do_dźwigu_rozpoznanie_bojem'           : OrderedDict([(20,10)]),
            'v_nie_gaśnicza_wewn_poziom_dym0'                       : 1.33,
            'v_zewn'                                                : 2,
            'v_nie_gaśnicza_wewn_pion_dym0'                         : OrderedDict([(12,100), (25,220), (55,1060)]),
            't_wyważanie_drzwi_drewniane_dym0'                      : 80,
            't_wyważanie_drzwi_drewniane_dym1'                      : 170,
            't_wyważanie_drzwi_antywłamaniowe_dym0'                 : 450,
            't_wyważanie_drzwi_antywłamaniowe_dym1'                 : 740,

        }

# }}}
    def make_segments_map(self):# {{{

        self.segments_map={
            '0000000000000001': 'wewn_dym0_poziom',
            '0000000000000101': 'wewn_dym0_pion',
            '0000000000001001': 'wewn_dym0_dzwig',
            '0000000000010001': 'wewn_dym0_hydrant',
            '0000000000000011': 'wewn_dym1_poziom',
            '0000000000000111': 'wewn_dym1_pion',
            '0000000000001011': 'wewn_dym1_dzwig',
            '0000000000010011': 'wewn_dym1_hydrant',
            '0000001100000000': 'zewn_poziom',
            '0000010100000000': 'zewn_drabina_przystawna',
            '0000100100000000': 'zewn_drabina_mechaniczna',
        }
# }}}
    def save(self,results):# {{{
        # TODO: Nie mogę polegać na plik_2021-01-07.15:30, bo muszę go odnaleźć i do tego ewentualnie wybrać z podobnych plików

        x=json.dumps({'results': results, 'conf': self.conf})
        if self.conf['start'] == 1:
            with open('wyniki.txt', "w") as f: 
                f.write(x+"\n") 
        else:
            with open('wyniki.txt', "a") as f: 
                f.write(x+"\n")
# }}}

    def czy_wykluczamy_bo_droga(self,wariant,data):# {{{
        # TODO: jak sumujemy suma_segmentow, bo duże długości mamy
        total_w52=0
        total_w75=0
        for s in self.conf['samochody']:
            total_w52 += int(self.s.query("select w_52,w_75 from Generics where id=?", (s['id'],))[0]['w_52'])
            total_w75 += int(self.s.query("select w_52,w_75 from Generics where id=?", (s['id'],))[0]['w_75'])
        total = total_w75 + total_w52

        suma_segmentow=0
        for i in data['segmenty']:
            suma_segmentow += i['długość']

        if suma_segmentow > total:
            #print(suma_segmentow, total)
            return 1
        else:
            return 0
# }}}
    def czy_wykluczamy(self,wariant,data):# {{{
        if self.czy_wykluczamy_bo_droga(wariant,data) == 1:
            return 1
# }}}

    def wewn_dym0_poziom(self, segment):# {{{
        # TODO: kiedy która prędkość?

        #  bit1=1  rozwinięcie podstawowe
        if segment['wariant'][-2] == '1':
            if self.weze_nawodnione == 1:
                return segment['długość'] / self.query("v_linia_gaśn_w52_wewn_poziom_dym0_kregi", segment['długość'])
            else:
                return segment['długość'] / self.query("v_rota_gaśn_wewn_poziom_dym0", segment['długość'])

        #  bit1=0  rozwinięcie niepodstawowe, czyli gaśnica?
        else:
            return segment['długość'] / self.query("v_rota_gaśn_wewn_poziom_dym0", segment['długość'])
# }}}
    def wewn_dym0_pion(self, segment):# {{{
        # TODO: kiedy która prędkość?
        # 'v_nie_gaśnicza_wewn_pion_dym0'                         : OrderedDict([(12,100), (25,220), (55,1060)]),

        #  bit1=1  rozwinięcie podstawowe
        if segment['wariant'][-2] == '1':
            if self.weze_nawodnione == 1:
                return self.query("t_linia_gaśn_w52_wewn_pion_dym0_kregi_1rota", segment['długość'])
            else:
                return self.query("t_rota_gaśn_wewn_pion_dym0", segment['długość'])


        #  bit1=0  rozwinięcie niepodstawowe, czyli gaśnica?
        else:
            return self.query("t_rota_gaśn_wewn_pion_dym0", segment['długość'])
# }}}
    def wewn_dym0_dzwig(self, segment):# {{{
        pieter_w_podrozy=segment['długość'] / 3
        pieter_w_budynku=self.conf['ogólne']['liczba_pięter']
        return 60 * pieter_w_podrozy / pieter_w_budynku
# }}}
    def wewn_dym0_hydrant(self, segment):# {{{
        # 't_sprawianie_hydrantu_podziemnego'                     : 70,
        # 't_sprawianie_hydrantu_naziemnego'                      : 30,
        self.weze_nawodnione=1
        return 30
        
# }}}
    def wewn_dym1_poziom(self, segment):# {{{
        #  bit1=1  rozwinięcie podstawowe
        if segment['wariant'][-2] == '1':
            if self.weze_nawodnione == 1:
                return segment['długość'] / self.query("v_linia_gaśn_w52_wewn_poziom_dym1_kregi", segment['długość'])
            else:
                return segment['długość'] / self.query("v_rota_gaśn_wewn_poziom_dym1", segment['długość'])

        #  bit1=0  rozwinięcie niepodstawowe, czyli gaśnica?
        else:
            return segment['długość'] / self.query("v_rota_gaśn_wewn_poziom_dym1", segment['długość'])
# }}}
    def wewn_dym1_pion(self, segment):# {{{
        # TODO: kiedy która prędkość?

        #  bit1=1  rozwinięcie podstawowe
        if segment['wariant'][-2] == '1':
            if self.weze_nawodnione == 1:
                return self.query("t_linia_gaśn_w52_wewn_pion_dym1_kregi_1rota", segment['długość'])
            else:
                return self.query("t_rota_gaśn_wewn_pion_dym1", segment['długość'])


        #  bit1=0  rozwinięcie niepodstawowe, czyli gaśnica?
        else:
            return self.query("t_rota_gaśn_wewn_pion_dym1", segment['długość'])
# }}}
    def wewn_dym1_dzwig(self, segment):# {{{
        pieter_w_podrozy=segment['długość'] / 3
        pieter_w_budynku=self.conf['ogólne']['liczba_pięter']
        return 60 * pieter_w_podrozy / pieter_w_budynku
# }}}
    def wewn_dym1_hydrant(self, segment):# {{{
        # TODO: skąd dane?
        dd(segment)
# }}}
    def zewn_poziom(self, segment):# {{{
        return segment['długość'] / self.query("v_zewn", segment['długość'])
# }}}
    def zewn_drabina_przystawna(self,segment):# {{{
        zdjecie_drabiny=60 
        bieg_z_drabina=segment['długość'] * 1.36
        drabine_spraw=190
        wspinaczka=20

        return zdjecie_drabiny + bieg_z_drabina + drabine_spraw + wspinaczka
# }}}
    def zewn_drabina_mechaniczna(self, segment):# {{{
        # TODO, sprawdzić
        # 't_przygotowanie_działań_drabina_mechaniczna'           : OrderedDict([(12,160), (25,180), (55,400)]),
        # 't_przygotowanie_asekuracji_drabina_mechaniczna'        : OrderedDict([(12,140), (25,160), (55,380)]),

        if segment['wariant'][-9] == '1':
            return self.query("t_przygotowanie_asekuracji_drabina_mechaniczna", segment['długość'])
        else:
            return self.query("t_przygotowanie_działań_drabina_mechaniczna", segment['długość'])
# }}}

    def main(self):# {{{
        self.weze_nawodnione=0
        xj=self.json.read('scenariusz.json')
        self.warianty=xj['warianty'] 
        self.conf=xj['conf']
        results=OrderedDict()
        for wariant,data in self.warianty.items():
            if self.czy_wykluczamy(wariant,data) == 1:
                continue
            czas_wariantu=0
            debug=[]
            for s in data['segmenty']:
                if s['segment'] not in self.segments_map:
                    #print("ignoruję nierozpoznany segment: {}".format(s['segment']))
                    debug.append('{},s:{},t:{} '.format(s['segment'],None,None))
                    continue
                else:
                    #s['segment']='0000010100000000' # temp zewn_drabina_przystawna()
                    #s['segment']='0000000000000001' # temp wewn_dym0_poziom()
                    #s['segment']='0000000000001001' # temp wewn_dym0_dzwig()
                    #s['segment']='0000000000010001' # temp wewn_dym0_hydrant()
                    s['segment']='0000100100000000' #'zewn_drabina_mechaniczna()

                    handler=getattr(self, self.segments_map[s['segment']])
                    s['segmentx']=self.segments_map[s['segment']]
                    s['wariant']=wariant
                    czas=handler(s)
                    czas_wariantu+=czas
                    debug.append('{},s:{},t:{} '.format(s['segmentx'],s['długość'],round(czas)))
            results[wariant]={ 'wynik':round(czas_wariantu), 'debug': debug}
        dd(results)
        self.save(results)
# }}}

d=DojazdMW()
