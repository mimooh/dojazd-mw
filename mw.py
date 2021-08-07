import sys
import os
import json
from collections import OrderedDict
from include import Json
from include import Dump as dd
from include import Sqlite

# todo{{{

# noszaki = 0.9 * kregi 
# OK, w db

# * ile m węża wykorzystano na zewn w poziomie łącznie % węży używamy w praktyce 
# * ile m węża wykorzystano na wewn łącznie OK
# OK: self.raport_potrzeb + w db

# podnosnik vs drabina
# OK

# naprawić wysokość piętra 
# OK

# poprosic x-code o wyrzucenie pion/poziom
# '0000000000010001': 'wewn_dym0_hydrant',
# '0000000000010001': 'wewn_dym0_hydrant',
# '0000000000010011': 'wewn_dym1_hydrant',

# '0000000000100001': 'wewn_dym0_poziom_lina_elewacja',
# '0000000000100011': 'wewn_dym1_poziom_lina_elewacja',
# '0000000000100101': 'wewn_pion_lina_elewacja',

# wskazac X-code konkretny scenariusz
# {'segment_status': 'OK' , 'segment': '0000000000010001' , 'funkcja': 'wewn_dym0_hydrant' , 'czas': 30 , 'nawodniona': 1}
# {'segment_status': 'OK' , 'segment': '0000000000010101' , 'funkcja': 'wewn_dym0_hydrant' , 'czas': 30 , 'nawodniona': 1}
# {'segment_status': 'OK' , 'segment': '0000000000010001' , 'funkcja': 'wewn_dym0_hydrant' , 'czas': 30 , 'nawodniona': 1}
# {'segment_status': 'OK' , 'segment': '0000000000010101' , 'funkcja': 'wewn_dym0_hydrant' , 'czas': 30 , 'nawodniona': 1}


# }}}

class DojazdMW:
    def __init__(self):# {{{
        if len(sys.argv) < 2:
            self.zbior='office123/sesja1'
            self.debugging=1
        else:
            self.zbior=sys.argv[1]
            self.debugging=0

        self.json=Json()
        self.debug("symulacje/{}/scenariusz.json".format(self.zbior))
        self.debug("symulacje/{}/wyniki.txt".format(self.zbior))
        self.make_segments_map()
        self.make_db_czynnosci()
        self.s=Sqlite("sqlite/firetrucks.db")
        self.main()
# }}}
    def query(self, param, dlugosc=0):# {{{
        '''
        query odpowiada wartością lub trafia na dict opisany poniżej:
        query('t_rota_gaśn_wewn_pion_dym1', 6)

        if isinstance(self.db_czynnosci[param], dict):
            't_rota_gaśn_wewn_pion_dym0': OrderedDict([(12,100),(25,330),(55,1026)])
            6 jest w przedziale (do 12m, 100 sekund)
            czyli 100 * 6/12 
        '''

        if isinstance(self.db_czynnosci[param], dict):
            for metry in list(self.db_czynnosci[param].keys()):
                if metry >= dlugosc:
                    return self.db_czynnosci[param][metry] * dlugosc/metry
        else:
            return self.db_czynnosci[param]

# }}}
    def make_sis(self):# {{{
        self.sis={ 'total_w52': 0, 'total_w75': 0, 'jest_drabina_mechaniczna': 0, 'jest_podnosnik': 0, 'załoga':0 }
        for s in self.conf['samochody']:
            self.sis['total_w52'] += int(self.s.query("select w_52 from Generics where id=?", (s['id'],))[0]['w_52'])
            self.sis['total_w75'] += int(self.s.query("select w_75 from Generics where id=?", (s['id'],))[0]['w_75'])

        self.sis['total_w52'] *= self.query("skaluj_efektywne_sis_w52")
        self.sis['total_w75'] *= self.query("skaluj_efektywne_sis_w75")

        for i in self.conf['samochody']:
            if i['id'] == 'gen5':
                self.sis['jest_drabina_mechaniczna']=1
            if i['id'] == 'gen6':
                self.sis['jest_podnosnik']=1
            self.sis['załoga']+=i['załoga']
# }}}
    def make_db_czynnosci(self):# {{{
        self.db_czynnosci={
            'skaluj_efektywne_sis_w52'                              : 0.9,
            'skaluj_efektywne_sis_w75'                              : 0.9,
            'skaluj_działania_noszaki_przez_działania_kregi'        : 0.8,
            't_przejazd_dzwig_ostatnia_kondygnacja'                 : 60,
            't_pkt_sprawianie_hydrantu_podziemnego_zewn_dym0'       : 70,
            't_pkt_sprawianie_hydrantu_naziemnego_zewn_dym0'        : 30,
            't_pkt_sprawianie_hydrantu_wewn_dym0'                   : 30,
            't_pkt_sprawianie_hydrantu_wewn_dym1'                   : 60,
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
            't_drabina_przystawna_zdjecie'                          : 60,
            't_drabina_przystawna_sprawianie'                       : 190,
            't_drabina_przystawna_wspinanie'                        : 20,
            'v_drabina_przystawna_bieg'                             : 1.36,
            't_drabina_przystawna_przygotowanie_asekuracji'         : OrderedDict([(20,220)]),
            't_przygotowanie_działań_drabina_mechaniczna'           : OrderedDict([(12,160), (25,180), (55,400)]),
            't_przygotowanie_działań_podnośnik'                     : OrderedDict([(12,250), (25,290), (55,490)]),
            't_przygotowanie_sprzęt_wentylacja'                     : OrderedDict([(20,120)]),
            't_przygotowanie_roty_gotowość'                         : 25,
            't_przygotowanie_medyczne'                              : 70,
            't_przygotowanie_monitorowania_aparatów_powietrznych'   : 30,
            't_zabezpieczenie_pachołkami'                           : 170,
            't_rozpoznanie_wstepne_3600'                            : 70,
            't_przygotowanie_asekuracji_drabina_mechaniczna'        : OrderedDict([(12,140), (25,160), (55,380)]),
            't_przygotowanie_asekuracji_podnośnik'                  : OrderedDict([(12,230), (25,260), (55,460)]),
            't_przygotowanie_skokochronu'                           : OrderedDict([(20,130)]),
            't_przygotowanie_asekuracji_rota_RIT'                   : 110,
            't_dotarcie_roty_do_dźwigu_rozpoznanie_bojem'           : OrderedDict([(20,10)]),
            'v_nie_gaśnicza_wewn_poziom_dym0'                       : 1.33,
            'v_zewn_poziom'                                         : 2,
            'v_zewn_pion'                                           : 1.5,
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
            '0000000000001011': 'wewn_dym1_dzwig',
            '0000000000000011': 'wewn_dym1_poziom',
            '0000000000000111': 'wewn_dym1_pion',
            '0000001100000000': 'zewn_poziom',
            '0000010100000000': 'zewn_drabina_przystawna',
            '0000100100000000': 'zewn_drabina_mechaniczna',
            '0000000100000000': 'zewn_pion',
            '0000000000010101': 'wewn_dym0_hydrant',
            '0000000000010001': 'wewn_dym0_hydrant',
            '0000000000010011': 'wewn_dym1_hydrant',
            '0000000000100001': 'wewn_dym0_poziom_lina_elewacja',
            '0000000000100011': 'wewn_dym1_poziom_lina_elewacja',
            '0000000000100101': 'wewn_pion_dym0_lina_elewacja',
        }
# }}}
    def save_interaktywny(self,udane):# {{{
        collect=[]
        for x,z in udane['warianty'].items():
            collect.append([z['czas'], z['wariant']])
        c=sorted(collect)
        out=OrderedDict()
        for i in c:
            out[i[1]]=i[0]
        print(json.dumps(out))
# }}}
    def save(self,udane):# {{{
        if self.conf['tryb'] == 'interaktywny':
            self.save_interaktywny(udane)
        else:
            x=json.dumps({'results': udane, 'xy_samochody': self.conf['ogólne']['xy_samochody'], 'xyz_pozar': self.conf['pożar']['xyz']})
            if self.conf['status'] == 'Start':
                with open('symulacje/{}/wyniki.txt'.format(self.zbior), "w") as f: 
                    f.write(x+"\n") 
                with open('symulacje/{}/conf.txt'.format(self.zbior), "w") as f: 
                    conf=json.dumps({'conf': self.conf})
                    f.write(conf+"\n") 
            else:
                with open('symulacje/{}/wyniki.txt'.format(self.zbior), "a") as f: 
                    f.write(x+"\n")

            if self.conf['status'] == 'Koniec':
                os.system("python3 results.py '{}'".format(self.zbior))

# }}}
    def czy_wykluczamy_wariant_bo_droga(self,wariant,data):# {{{
        potrzeba_w52=0
        potrzeba_w75=0
        for i in data['segmenty']:
            if i['segment'][-1] == '1':
                potrzeba_w52 += i['długość']
            if i['segment'][-1] == '0':
                potrzeba_w75 += i['długość']

        self.raport_potrzeb={ 'w52': potrzeba_w52, 'w75': potrzeba_w75 }

        if potrzeba_w52 > self.sis['total_w52']:
            return { "status": "ERR", "debug":  "Długość segmentów wewnątrz {}[m] przekracza sis_w52 {}[m]".format(round(potrzeba_w52), self.sis['total_w52']) }

        if potrzeba_w75 > self.sis['total_w75']:
            return { "status": "ERR", "debug":  "Długość segmentów na zewnątrz {}[m] przekracza sis_w75 {}[m]".format(round(potrzeba_w75), self.sis['total_w75']) }

        return { "status": "OK" }
# }}}
    def czy_wykluczamy_wariant(self,wariant,data):# {{{
        x=self.czy_wykluczamy_wariant_bo_droga(wariant,data)
        if x['status'] == "ERR":
            return x
        return { "status": "OK" }

        # czy_wykluczamy_wariant_bo_zaloga()
# }}}

    def wewn_dym0_poziom(self, segment):# {{{
        # 0000001000000001 1/10
        # 0000000000000011 1/10

        # xxxxxx11 
        # xxxxxx01 

        # TODO: kiedy która prędkość? 

        #  bit1=1  rozwinięcie podstawowe
        if segment['wariant'][-2] == '1':
            if self.weze_nawodnione == 1:
                return segment['długość'] / self.query("v_linia_gaśn_w52_wewn_poziom_dym0_kregi", segment['długość'])
            else:
                return segment['długość'] / self.query("v_rota_gaśn_wewn_poziom_dym0", segment['długość'])

        #  000000000000

        #  bit1=0  rozwinięcie niepodstawowe, czyli gaśnica?
        else:
            return segment['długość'] / self.query("v_rota_gaśn_wewn_poziom_dym0", segment['długość'])
# }}}
    def wewn_dym1_poziom(self, segment):# {{{
        # 0000000000000011 0/10
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
    def wewn_dym0_pion(self, segment):# {{{
        # 0000000000000101 1/10

        # TODO: kiedy która prędkość? 1/10
        # 'v_nie_gaśnicza_wewn_pion_dym0' : OrderedDict([(12,100), (25,220), (55,1060)]),

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
    def wewn_dym1_pion(self, segment):# {{{
        # 0000000000000111 1/10
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
    def wewn_dym0_dzwig(self, segment):# {{{
        # 0000000000001001 8/10
        conf=OrderedDict()
        conf['długość']=segment['długość']
        conf['wysokość_budynku']=self.conf['ogólne']['wysokość_budynku']
        conf['t_ostatnia']=self.query("t_przejazd_dzwig_ostatnia_kondygnacja")
        conf['t']=conf['t_ostatnia'] * conf['długość'] / conf['wysokość_budynku']
        return conf['t']
# }}}
    def wewn_dym1_dzwig(self, segment):# {{{
        # 0000000000001011 8/10
        conf=OrderedDict()
        conf['długość']=segment['długość']
        conf['pieter_w_podrozy']=segment['długość'] / 3
        conf['pieter_w_budynku']=self.conf['ogólne']['liczba_pięter']
        conf['t']=self.query("t_przejazd_dzwig_ostatnia_kondygnacja")
        return conf['t'] * conf['pieter_w_podrozy'] / conf['pieter_w_budynku']
# }}}
    def wewn_dym0_hydrant(self, segment):# {{{
        # 0000000000010001 9/10
        self.weze_nawodnione=1
        return self.query("t_pkt_sprawianie_hydrantu_wewn_dym0")
# }}}
    def wewn_dym1_hydrant(self, segment):# {{{
        # 0000000000010011 9/10
        self.weze_nawodnione=1
        return self.query("t_pkt_sprawianie_hydrantu_wewn_dym1")
        
# }}}
    def zewn_poziom(self, segment):# {{{
        # 10/10
        return segment['długość'] / self.query("v_zewn_poziom", segment['długość'])
# }}}
    def zewn_pion(self, segment):# {{{
        # 0000000100000000 5/10
        # analiza wariantu czy idzie (gaśnica, wciąganie po elewacji, hydrant wewn) czy rozwija

        return segment['długość'] / self.query("v_zewn_pion", segment['długość'])
# }}}
    def zewn_drabina_przystawna(self,segment):# {{{
        # 0000010100000000 9/10
        # dodać 2 przypadki z drabiny_mechanicznej bity wariantu -9 i -11
        zdjecie_drabiny=self.query("t_drabina_przystawna_zdjecie")
        bieg_z_drabina=segment['długość'] * self.query("v_drabina_przystawna_bieg")
        drabine_spraw=self.query("t_drabina_przystawna_sprawianie")
        wspinaczka=self.query("t_drabina_przystawna_wspinanie")

        return zdjecie_drabiny + bieg_z_drabina + drabine_spraw + wspinaczka
# }}}
    def zewn_drabina_mechaniczna(self, segment):# {{{
        # 0000100100000000 5/10

        if self.sis['jest_drabina_mechaniczna'] == 1:
            QQ='t_przygotowanie_działań_drabina_mechaniczna'
        else:
            QQ='t_przygotowanie_działań_podnośnik'

        # return None spowoduje odrzucenie wariantu, nie chcemy poniżej None w arytmetyce
        if self.query(QQ, segment['długość']) == None:
            return None

        # gaszenie z drabiny dużą wydajnością, scenariusz.json musi przekazywać czas_duza_woda
        if (segment['wariant'][-11] == '1' or segment['wariant'][-12] == '1') and (segment['wariant'][-16] == '1'):
            czas_duza_woda=1200 
            return czas_duza_woda + self.query(QQ, segment['długość'])

        # gaszenie z drabiny lub podnośnika
        if segment['wariant'][-11] == '1' or segment['wariant'][-12] == '1': 
            return self.query(QQ, segment['długość'])

        # strażak wchodzi przez okno z drabiny
        if segment['wariant'][-9] == '1': 
            return self.query("t_przygotowanie_roty_gaśn") + self.query(QQ, segment['długość'])
        

# }}}

    def wewn_dym0_poziom_lina_elewacja(self, segment):# {{{
        # 0000000000100001 0/10
        # todo jest to punkt, jak hydrant, nazwać punkt, 
        return 0
# }}}
    def wewn_dym1_poziom_lina_elewacja(self, segment):# {{{
        # todo
        return 0
# }}}
    def wewn_pion_dym0_lina_elewacja(self, segment):# {{{
        return 0
    # }}}

    def debug(self,msg):# {{{
        if self.debugging == 1:
            print(msg)
# }}}
    def main_process_segment(self, wariant, s):# {{{
        #s['segment']='0000000000001011' # 'wewn_dym1_dzwig()
        #s['segment']='0000000000010101' # 'wewn_dym0_hydrant',
        #s['segment']='0000000000010011' # 'wewn_dym1_hydrant',
        #s['segment']='0000010100000000' # 'zewn_drabina_przystawna',
        #s['segment']='0000100100000000' # 'zewn_drabina_mechaniczna'

        if s['segment'] not in self.segments_map:
            return { "segment_status": "ERR", "debug": "{}: nieznany segment".format(s['segment']) }
        funkcja=self.segments_map[s['segment']]
        handler=getattr(self, funkcja)
        s['wariant']=wariant
        czas=handler(s)
        if czas == None:
            return { 'segment_status': "ERR", 'segment': s['segment'], 'funkcja': funkcja, 'długość': round(s['długość']), 'debug': "None dla długości: {}, db_err ?".format(s['długość']) }
        return { "segment_status": "OK", "segment": s['segment'], 'funkcja': funkcja, "długość": round(s['długość']), "czas": round(czas), "nawodniona": self.weze_nawodnione }
# }}}
    def main_process_wariant(self, wariant, data):# {{{
        self.weze_nawodnione=0
        czas_wariantu=0
        if self.debugging == 1:
            print("\nwariant", wariant)
        xx=self.czy_wykluczamy_wariant(wariant,data)
        if xx['status'] == 'ERR':
            return { "wariant_status": "ERR", "wynik": None, "debug": xx['debug'] }
        for segment in data['segmenty']:
            x=self.main_process_segment(wariant,segment)
            self.debug(x)
            if x['segment_status'] == "OK":
                czas_wariantu+=x['czas']
            else:
                return { 'wariant_status': "ERR", "debug": x['debug'] }
        return { 'wariant_status': "OK", "wariant": wariant, 'czas':round(czas_wariantu) }
# }}}
    def main(self):# {{{
        xj=self.json.read('symulacje/{}/scenariusz.json'.format(self.zbior))
        self.warianty=xj['warianty'] 
        self.conf=xj['conf']
        self.make_sis()
        udane=OrderedDict()
        udane['best']={ 'wariant': None, 'czas': 9999999999 }
        udane['warianty']=OrderedDict()
        nieudane=OrderedDict()
        for wariant,data in self.warianty.items():
            w=self.main_process_wariant(wariant,data)
            self.debug(w)
            if w['wariant_status'] == 'OK':
                udane['warianty'][wariant]=w
                if w['czas'] < udane['best']['czas']:
                    udane['best']={ 'wariant': wariant, 'czas': w['czas'] }
            else:
                nieudane[wariant]=w

        if self.debugging == 1:
            print("\nBest:"    , udane['best'])
            dd("Warianty OK:"  , udane['warianty'])
            dd("Warianty ERR:" , nieudane)
        self.save(udane)
# }}}

d=DojazdMW()

# symulacje/office123/sesja1/wyniki.txt
# symulacje/office123/sesja1/scenariusz.json
