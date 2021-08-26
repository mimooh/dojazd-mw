import sys
import os
import json
from collections import OrderedDict
from include import Json
from include import Dump as dd
from include import Sqlite

# wciaganie po elewacji segement to składowa pionowa
# drabina segment vs wariant bład w scenariusz.json

class DojazdMW:
    def __init__(self):# {{{
        if len(sys.argv) < 2:
            self.zbior='symulacje/office123/sesja1'
            self.debugging=1
        else:
            self.zbior=sys.argv[1]
            self.debugging=0

        self.json=Json()
        self.debug("{}/scenariusz.json".format(self.zbior))
        self.debug("{}/wyniki.txt".format(self.zbior))
        self.debug("{}/wynik_interaktywny.json".format(self.zbior))
        self.make_maps()
        self.make_db_czynnosci()
        self.s=Sqlite("sqlite/firetrucks.db")
        self.main()
# }}}
    def query_przedzialy(self, param, dlugosc):# {{{
        '''
        Przedzialy sa liniowe, ale tylko pierwszy (i=0) jest trywialny
        '''

        i=0
        for limit,wynik in self.db_czynnosci[param]:
            if dlugosc <= limit  and i==0:
                return wynik * dlugosc/limit
            else:
                if dlugosc <= limit:
                    x0=self.db_czynnosci[param][i-1][0]
                    y0=self.db_czynnosci[param][i-1][1]
                    x1=self.db_czynnosci[param][i][0]
                    y1=self.db_czynnosci[param][i][1]
                    wynik = y0 + ((y1 - y0) * (dlugosc - x0) ) / (x1 - x0)
                    return wynik * dlugosc/limit
            i+=1
        return None
# }}}
    def query(self, param, dlugosc=0):# {{{
        '''
        query odpowiada wartoscia lub trafia na liste przedzialow i do query_przedzialy()
        sin(38)=0.615 in caller() sluzy do wyciagania skladowej pionowej
        '''

        if isinstance(self.db_czynnosci[param], list):
            return self.query_przedzialy(param,dlugosc)
        else:
            return self.db_czynnosci[param]

# }}}
    def make_sis(self):# {{{
        self.sis={ 'total_w52': 0, 'total_w75': 0, 'jest_drabina_mechaniczna': 0, 'jest_podnosnik': 0, 'zaloga':0 }
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
            self.sis['zaloga']+=i['zaloga']
# }}}

    def make_db_czynnosci(self):# {{{
        self.db_czynnosci={
            'skaluj_efektywne_sis_w52'                              : 0.9,
            'skaluj_efektywne_sis_w75'                              : 0.9,
            'skaluj_dzialania_noszaki_przez_dzialania_kregi'        : 0.8,
            't_przejazd_dzwig_ostatnia_kondygnacja'                 : 60,
            't_sprawianie_hydrantu_wewn_dym0'                       : 30,
            't_sprawianie_hydrantu_wewn_dym1'                       : 60,
            't_przygotowanie_roty_gasn'                             : 50,
            'v_duza_woda'                                           : 1.4,

            'v_linia_glowna_w75_do_rozdzielacza_poziom'             : 0.66,
            'v_linia_glowna_w75_do_rozdzielacza_pion'               : 0.5,
            'v_bez_weza_zewn_poziom_dym0'                           : 2,
            'v_bez_weza_zewn_pion_dym0'                             : 1.5,
            'v_bez_weza_wewn_poziom_dym0'                           : 1.33,
            'v_bez_weza_wewn_poziom_dym1'                           : 0.4,
            't_bez_weza_wewn_pion_dym0'                             : [(12 , 100) , (25 , 220) , (55 , 1060)] ,
            't_bez_weza_wewn_pion_dym1'                             : [(12 , 140) , (25 , 310) , (55 , 1500)]  ,
            'v_rozwijanie_kregi_wewn_poziom_dym0'                   : 0.8 ,
            'v_rozwijanie_kregi_wewn_poziom_dym1'                   : 0.5 ,
            't_rozwijanie_kregi_wewn_pion_dym0'                     : [(12 , 200) , (25 , 700)  , (55 , 1500)] ,
            't_rozwijanie_kregi_wewn_pion_dym1'                     : [(12 , 280) , (25 , 1000) , (55 , 2100)] ,
            'v_poruszenie_weze_nawodnione_wewn_poziom_dym0'         : 0.5,
            'v_poruszenie_weze_nawodnione_wewn_poziom_dym1'         : 0.2,
            'v_poruszenie_weze_nawodnione_wewn_pion_dym0'           : 0.4,
            'v_poruszenie_weze_nawodnione_wewn_pion_dym1'           : 0.1,
            't_linia_gasn_w52_elewacja_dym0'                        : [(12,440),(25,880),(55,2120)],
            't_linia_gasn_w52_elewacja_dym1'                        : [(12,999999),(25,99999999),(55,999999)],

            't_drabina_przystawna_zdjecie'                          : 60,
            't_drabina_przystawna_sprawianie'                       : 190,
            't_drabina_przystawna_wspinanie'                        : 20,
            'v_drabina_przystawna_bieg'                             : 1.36,
            't_drabina_przystawna_przygotowanie_asekuracji'         : [(20,220)],
            't_przygotowanie_dzialan_drabina_mechaniczna'           : [(12,160), (25,180), (55,400)],
            't_przygotowanie_dzialan_podnosnik'                     : [(12,250), (25,290), (55,490)],

            't_sprawianie_hydrantu_podziemnego_zewn_dym0'           : 70,
            't_sprawianie_hydrantu_naziemnego_zewn_dym0'            : 30,
            't_zasilenie_samochodu'                                 : [(20,30)],
            't_zasilenie_instalacji_w75x1'                          : [(20,70)],
            't_zasilenie_instalacji_w75x2'                          : [(20,100)],
            't_sprawianie_motopompy_MP81_z_linia_w75'               : [(20,320)],
            't_sprawianie_motopompy_szlam_z_linia_w75'              : [(20,510)],
            't_sprawianie_zbiornika_2i5m3'                          : 290,
            't_sprawianie_zbiornika_5m3'                            : 150,
            't_linia_glowna_w75x2_do_rozdzielacza_harmonijka'       : 15,
            'v_rota_gasn_zewn_poziom_dym0'                          : 1,
            'v_rota_gasn_wewn_poziom_dym0'                          : 0.8,
            'v_rota_gasn_wewn_poziom_dym1'                          : 0.38,
            't_rota_gasn_wewn_pion_dym0'                            : [(12,100),(25,330),(55,1026)],
            't_rota_gasn_wewn_pion_dym1'                            : [(12,140),(25,500),(55,1520)],
            'v_linia_gasn_w52_wewn_poziom_dym1_kregi'               : 0.25,
            't_linia_gasn_w52_wewn_pion_dym1_kregi_1rota'           : [(12,620),(25,1120),(55,2120)],
            't_linia_gasn_w52_wewn_pion_dym1_kregi_2roty'           : [(12,500),(25,1060),(55,1520)],
            'v_linia_gasn_w52_wewn_poziom_dym0_kregi'               : 0.8,
            't_linia_gasn_w52_wewn_pion_dym0_kregi_1rota'           : [(12,230),(25,760),(55,1700)],
            't_linia_gasn_w52_wewn_pion_dym0_kregi_2roty'           : [(12,170),(25,700),(55,1520)],
            'v_linia_gasn_w42_wewn_poziom_dym1_kregi'               : 0.26,
            't_linia_gasn_w42_wewn_pion_dym1_kregi_1rota'           : [(12,620),(25,1120),(55,2120)],
            't_linia_gasn_w42_wewn_pion_dym1_kregi_2roty'           : [(12,500),(25,1060),(55,1520)],
            'v_linia_gasn_w42_wewn_poziom_dym0_kregi'               : 1,
            't_linia_gasn_w42_wewn_pion_dym0_kregi_1rota'           : [(12,230),(25,760),(55,1700)],
            't_linia_gasn_w42_wewn_pion_dym0_kregi_2roty'           : [(12,170),(25,700),(55,1520)],
            'v_linia_gasn_w52_wewn_poziom_dym1_kasetony'            : 0.4,
            't_linia_gasn_w52_wewn_pion_dym1_kasetony_1rota'        : [(12,560),(25,1000),(55,1940)],
            't_linia_gasn_w52_wewn_pion_dym1_kasetony_2roty'        : [(12,320),(25,880),(55,1510)],
            'v_linia_gasn_w52_wewn_poziom_dym0_kasetony'            : 1,
            't_linia_gasn_w52_wewn_pion_dym0_kasetony_1rota'        : [(12,500),(25,940),(55,1880)],
            't_linia_gasn_w52_wewn_pion_dym0_kasetony_2roty'        : [(12,320),(25,700),(55,1510)],
            'v_linia_gasn_w42_wewn_poziom_dym1_kasetony'            : 0.4,
            't_linia_gasn_w42_wewn_pion_dym1_kasetony_1rota'        : [(12,500),(25,940),(55,1940)],
            't_linia_gasn_w42_wewn_pion_dym1_kasetony_2roty'        : [(12,320),(25,880),(55,1510)],
            'v_linia_gasn_w42_wewn_poziom_dym0_kasetony'            : 1.33,
            't_linia_gasn_w42_wewn_pion_dym0_kasetony_1rota'        : [(12,500),(25,940),(55,1880)],
            't_linia_gasn_w42_wewn_pion_dym0_kasetony_2roty'        : [(12,320),(25,700),(55,1510)],
            't_linia_gasn_w52_wewn_pion_dym1_dusza_klatki_2roty'    : [(12,500),(25,940),(55,1940)],
            't_linia_gasn_w52_wewn_pion_dym1_dusza_klatki_3roty'    : [(12,320),(25,880),(55,1510)],
            't_linia_gasn_w52_wewn_pion_dym0_dusza_klatki_2roty'    : [(12,500),(25,940),(55,1880)],
            't_linia_gasn_w52_wewn_pion_dym0_dusza_klatki_3roty'    : [(12,320),(25,700),(55,1510)],
            't_linia_gasn_w42_wewn_pion_dym1_dusza_klatki_2roty'    : [(12,500),(25,940),(55,1940)],
            't_linia_gasn_w42_wewn_pion_dym1_dusza_klatki_3roty'    : [(12,320),(25,880),(55,1510)],
            't_linia_gasn_w42_wewn_pion_dym0_dusza_klatki_2roty'    : [(12,440),(25,940),(55,1880)],
            't_linia_gasn_w42_wewn_pion_dym0_dusza_klatki_3roty'    : [(12,320),(25,700),(55,1510)],
            't_szybkie_natarcie_zewn_poziom'                        : [(20,50)],
            't_szybkie_natarcie_zewn_pion_elewacja'                 : [(12,190)],
            't_linia_gasn_w42_elewacja'                             : [(12,430),(25,860),(55,1880)],
            't_przygotowanie_sprzet_wentylacja'                     : [(20,120)],
            't_przygotowanie_roty_gotowosc'                         : 25,
            't_przygotowanie_medyczne'                              : 70,
            't_przygotowanie_monitorowania_aparatow_powietrznych'   : 30,
            't_zabezpieczenie_pacholkami'                           : 170,
            't_rozpoznanie_wstepne_3600'                            : 70,
            't_przygotowanie_asekuracji_drabina_mechaniczna'        : [(12,140), (25,160), (55,380)],
            't_przygotowanie_asekuracji_podnosnik'                  : [(12,230), (25,260), (55,460)],
            't_przygotowanie_skokochronu'                           : [(20,130)],
            't_przygotowanie_asekuracji_rota_RIT'                   : 110,
            't_dotarcie_roty_do_dzwigu_rozpoznanie_bojem'           : [(20,10)],
            't_wywazanie_drzwi_drewniane_dym0'                      : 80,
            't_wywazanie_drzwi_drewniane_dym1'                      : 170,
            't_wywazanie_drzwi_antywlamaniowe_dym0'                 : 450,
            't_wywazanie_drzwi_antywlamaniowe_dym1'                 : 740,

        }

# }}}
    def make_maps(self):# {{{

        self.segments_map={
            '0000000000000001': 'wewn_poziom_dym0',
            '0000000000000011': 'wewn_poziom_dym1',
            '0000000000000101': 'wewn_pion_dym0',
            '0000000000000111': 'wewn_pion_dym1',
            '0000010100000000': 'zewn_drabina_przystawna',
            '0000100100000000': 'zewn_drabina_mechaniczna',
            '0000000100000000': 'zewn_pion',
            '0000001100000000': 'zewn_poziom',
            '0000000000010101': 'wewn_dym0_hydrant',
            '0000000000010001': 'wewn_dym0_hydrant',
            '0000000000010011': 'wewn_dym1_hydrant',
            '0000000000100001': 'wewn_dym0_lina_elewacja',
            '0000000000100011': 'wewn_dym1_lina_elewacja',
            '0000000000001001': 'wewn_dzwig',
            '0000000000001011': 'wewn_dzwig',
        }
        self.wariants_map={
            '0000000000000011': 'Wewnętrzne rozwinięcie gaśnicze od nasady tłocznej pompy',
            '0000000000001001': 'Rozwinięcie gaśnicze od hydrantu wewnętrznego',
            '0000000000000100': 'Działanie gaśnicze sprzętem podręcznym z wykorzystaniem dźwigu ratowniczego',
            '0000000000000000': 'Działanie gaśnicze sprzętem podręcznym',
            '0000000000010001': 'Rozwinięcie gaśnicze z wciąganiem linii wężowej po elewacji',
            '0000000000010101': 'Rozwinięcie gaśnicze z wciąganiem linii wężowej po elewacji z wykorzystaniem dźwigu ratowniczego',
            '0000001100000000': 'Gaszenie z poziomu ziemi',
            '0000010100000000': 'Gaszenie z drabiny przystawnej',
            '0000100100000000': 'Gaszenie z kosza drabiny lub podnośnika',
            '0000010100000001': 'Rozwinięcie gaśnicze z dostępem z drabiny przystawnej',
            '0000100100000001': 'Rozwinięcie gaśnicze z dostępem z kosza drabiny lub podnośnika'
        }
# }}}
    def save_interaktywny(self,udane,nieudane):# {{{
        collect=[]
        for x,z in udane['warianty'].items():
            collect.append((z['czas'], { 'wariant': z['wariant'], 'status': z['wariant_status'], 'wynik': z['czas']}))
        udane_sorted=sorted(collect, key=lambda x: x[0])
        out=OrderedDict()
        for a,b in udane_sorted:
            out[b['wariant']]={'status':b['status'], 'wynik':b['wynik']}
        for a,b in nieudane.items():
            out[a]={'status':"ERR: "+b['debug'], 'wynik':None }
        self.json.write(out, '{}/wynik_interaktywny.json'.format(self.zbior))

# }}}
    def save(self,udane,nieudane):# {{{
        if self.conf['tryb'] == 'interaktywny':
            self.save_interaktywny(udane,nieudane)
        else:
            x=json.dumps({'results': udane, 'xy_samochody': self.conf['ogolne']['xy_samochody'], 'xyz_pozar': self.conf['pozar']['xyz']})
            if self.conf['status'] == 'Start':
                with open('{}/wyniki.txt'.format(self.zbior), "w") as f: 
                    f.write(x+"\n") 
                with open('{}/conf.txt'.format(self.zbior), "w") as f: 
                    conf=json.dumps({'conf': self.conf})
                    f.write(conf+"\n") 
            else:
                with open('{}/wyniki.txt'.format(self.zbior), "a") as f: 
                    f.write(x+"\n")

            if self.conf['status'] == 'Koniec':
                os.system("python3 results.py {}".format(self.zbior))

# }}}
    def czy_wykluczamy_wariant_bo_droga(self,wariant,data):# {{{
        potrzeba_w52=0
        potrzeba_w75=0
        for i in data['segmenty']:
            if i['segment'][-1] == '1':
                potrzeba_w52 += i['dlugosc']
            if i['segment'][-1] == '0':
                potrzeba_w75 += i['dlugosc']

        self.raport_potrzeb={ 'w52': potrzeba_w52, 'w75': potrzeba_w75 }

        if potrzeba_w52 > self.sis['total_w52']:
            return { "status": "ERR", "debug":  "Dlugosc segmentow wewnatrz {}[m] przekracza sis_w52 {}[m]".format(round(potrzeba_w52), self.sis['total_w52']) }

        if potrzeba_w75 > self.sis['total_w75']:
            return { "status": "ERR", "debug":  "Dlugosc segmentow na zewnatrz {}[m] przekracza sis_w75 {}[m]".format(round(potrzeba_w75), self.sis['total_w75']) }

        return { "status": "OK" }
# }}}
    def czy_wykluczamy_wariant(self,wariant,data):# {{{
        x=self.czy_wykluczamy_wariant_bo_droga(wariant,data)
        if x['status'] == "ERR":
            return x
        return { "status": "OK" }

        # czy_wykluczamy_wariant_bo_zaloga()
# }}}
    def czy_rozwiniecie_wezowe(self, segment):# {{{
        # 0000000000000000 gasnica schodami (droga tak jak rozwiniecie podstawowe)
        # 0000000000000100 gasnica dzwigiem
        if self.weszlismy_oknem == 1:
            return 1 

        if self.sprawilismy_hydrant == 1:
            return 1 

        if segment['wariant'][-5] == '1' or segment['wariant'][-4] == '1' or segment['wariant'] == '0000000000000000' or segment['wariant'] == '0000000000000100' :
            return 0 # nie
        else:
            return 1 # tak
# }}}

    def wewn_poziom_dym0(self, segment):# {{{
        # 0000000000000001 9/10

        if self.czy_rozwiniecie_wezowe(segment) == 1:
            if self.weze_nawodnione == 1:
                return segment['dlugosc'] / self.query("v_poruszenie_weze_nawodnione_wewn_poziom_dym0", segment['dlugosc'])
            else:
                return segment['dlugosc'] / self.query("v_rozwijanie_kregi_wewn_poziom_dym0", segment['dlugosc'])
        else:
            return segment['dlugosc'] / self.query("v_bez_weza_wewn_poziom_dym0", segment['dlugosc'])
# }}}
    def wewn_poziom_dym1(self, segment):# {{{
        # 0000000000000011 9/10

        if self.czy_rozwiniecie_wezowe(segment) == 1:
            self.weze_nawodnione=1
            return segment['dlugosc'] / self.query("v_poruszenie_weze_nawodnione_wewn_poziom_dym1", segment['dlugosc'])
        else:
            return segment['dlugosc'] / self.query("v_bez_weza_wewn_poziom_dym1", segment['dlugosc'])

# }}}
    def wewn_pion_dym0(self, segment):# {{{
        # 0000000000000101 9/10

        if self.czy_rozwiniecie_wezowe(segment) == 1:
            if self.weze_nawodnione == 1:
                return segment['dlugosc'] / self.query("v_poruszenie_weze_nawodnione_wewn_pion_dym0", 0.615 * segment['dlugosc'])
            else:
                return self.query("t_rozwijanie_kregi_wewn_pion_dym0", 0.615 * segment['dlugosc'])
        else:
            return self.query("t_bez_weza_wewn_pion_dym0", 0.615 * segment['dlugosc'])

# }}}
    def wewn_pion_dym1(self, segment):# {{{
        # 0000000000000111 9/10

        if self.czy_rozwiniecie_wezowe(segment) == 1:
            self.weze_nawodnione=1
            return segment['dlugosc'] / self.query("v_poruszenie_weze_nawodnione_wewn_pion_dym1", 0.615 * segment['dlugosc'])
        else:
            return self.query("t_bez_weza_wewn_pion_dym1", 0.615 * segment['dlugosc'])
# }}}
    def zewn_poziom(self, segment):# {{{
        # 0000001100000000 9/10 

        if self.czy_rozwiniecie_wezowe(segment) == 1:
            return segment['dlugosc'] / self.query("v_bez_weza_zewn_poziom_dym0", segment['dlugosc'])
        else:
            return segment['dlugosc'] / self.query('v_linia_glowna_w75_do_rozdzielacza_poziom', segment['dlugosc'])

# }}}
    def zewn_pion(self, segment):# {{{
        # 0000000100000000 9/10
        
        if self.czy_rozwiniecie_wezowe(segment) == 1:
            return segment['dlugosc'] / self.query("v_bez_weza_zewn_pion_dym0", 0.615 * segment['dlugosc'])
        else:
            return segment['dlugosc'] / self.query('v_linia_glowna_w75_do_rozdzielacza_pion', 0.615 * segment['dlugosc'])
# }}}
    def wewn_dzwig(self, segment):# {{{
        # 0000000000001001 9/10

        conf=OrderedDict()
        conf['dlugosc']=segment['dlugosc']
        conf['wysokosc_budynku']=self.conf['ogolne']['wysokosc_budynku']
        conf['t_ostatnia']=self.query("t_przejazd_dzwig_ostatnia_kondygnacja")
        conf['t']=conf['t_ostatnia'] * conf['dlugosc'] / conf['wysokosc_budynku']
        return conf['t']
# }}}
    def wewn_dym0_hydrant(self, segment):# {{{
        # 0000000000010001 9/10
        self.weze_nawodnione=1
        self.sprawilismy_hydrant=1
        return self.query("t_sprawianie_hydrantu_wewn_dym0")
# }}}
    def wewn_dym1_hydrant(self, segment):# {{{
        # 0000000000010011 9/10
        self.weze_nawodnione=1
        self.sprawilismy_hydrant=1
        return self.query("t_sprawianie_hydrantu_wewn_dym1")
        
# }}}
    def zewn_drabina_przystawna(self,segment):# {{{
        # 0000010100000000 8/10

        zdjecie_drabiny=self.query("t_drabina_przystawna_zdjecie")
        bieg_z_drabina=segment['dlugosc'] * self.query("v_drabina_przystawna_bieg")
        drabine_spraw=self.query("t_drabina_przystawna_sprawianie")
        wspinaczka=self.query("t_drabina_przystawna_wspinanie")
        przygotowanie_roty=self.query("t_przygotowanie_roty_gasn")

        # gaszenie 
        if segment['wariant'][-11] == '1' or segment['wariant'][-12] == '1': 
            return zdjecie_drabiny + bieg_z_drabina + drabine_spraw + wspinaczka

        # strazak wchodzi przez okno 
        if segment['wariant'][-9] == '1': 
            self.weszlismy_oknem=1
            self.weze_nawodnione=1
            return zdjecie_drabiny + bieg_z_drabina + drabine_spraw + przygotowanie_roty + wspinaczka

# }}}
    def zewn_drabina_mechaniczna(self, segment):# {{{
        # 0000100100000000 9/10

        przygotowanie_roty=self.query("t_przygotowanie_roty_gasn")
        if self.sis['jest_drabina_mechaniczna'] == 1:
            przygotowanie_pojazdu=self.query('t_przygotowanie_dzialan_drabina_mechaniczna', segment['dlugosc'])
        else:
            przygotowanie_pojazdu=self.query('t_przygotowanie_dzialan_podnosnik', segment['dlugosc'])

        if przygotowanie_pojazdu == None:
            return None

        # gaszenie z drabiny duza wydajnoscia
        if (segment['wariant'][-11] == '1' or segment['wariant'][-12] == '1') and (segment['wariant'][-16] == '1'):
            czas_duza_woda=self.conf['ogolne']['odleglosc_duza_woda'] / self.query('v_duza_woda')
            return max(czas_duza_woda, przygotowanie_pojazdu)

        # gaszenie
        if segment['wariant'][-11] == '1' or segment['wariant'][-12] == '1': 
            return przygotowanie_pojazdu

        # strazak wchodzi przez okno
        if segment['wariant'][-9] == '1': 
            self.weszlismy_oknem=1
            self.weze_nawodnione=1
            return przygotowanie_roty + przygotowanie_pojazdu

# }}}
    def wewn_dym0_lina_elewacja(self, segment):# {{{
        # 0000000000100001 8/10

        self.weszlismy_oknem=1
        self.weze_nawodnione=1
        return self.query('t_linia_gasn_w52_elewacja_dym0', segment['dlugosc'])
# }}}
    def wewn_dym1_lina_elewacja(self, segment):# {{{
        # 0000000000100011 5/10  obliczyc dla dym1

        self.weszlismy_oknem=1
        self.weze_nawodnione=1
        return self.query('t_linia_gasn_w52_elewacja_dym1', segment['dlugosc'])
# }}}

    def debug(self,msg):# {{{
        if self.debugging == 1:
            print(msg)
# }}}
    def main_process_segment(self, wariant, s):# {{{
        #s['segment']='0000000000000001' # 'wewn_poziom_dym0',
        #s['segment']='0000000000000101' # 'wewn_pion_dym0',
        #s['segment']='0000000000001001' # 'wewn_dzwig',
        #s['segment']='0000000000001011' # 'wewn_dzwig',
        #s['segment']='0000000000000011' # 'wewn_poziom_dym1',
        #s['segment']='0000000000000111' # 'wewn_pion_dym1',
        #s['segment']='0000010100000000' # 'zewn_drabina_przystawna',
        #s['segment']='0000100100000000' # 'zewn_drabina_mechaniczna',
        #s['segment']='0000000100000000' # 'zewn_pion',
        #s['segment']='0000001100000000' # 'zewn_poziom',
        #s['segment']='0000000000010101' # 'wewn_dym0_hydrant',
        #s['segment']='0000000000010001' # 'wewn_dym0_hydrant',
        #s['segment']='0000000000010011' # 'wewn_dym1_hydrant',
        #s['segment']='0000000000100001' # 'wewn_dym0_lina_elewacja',
        #s['segment']='0000000000100011' # 'wewn_dym1_lina_elewacja',

        if s['segment'] not in self.segments_map:
            return { "segment_status": "ERR", "debug": "{}: nieobsługiwany segment".format(s['segment']) }
        funkcja=self.segments_map[s['segment']]
        handler=getattr(self, funkcja)
        s['wariant']=wariant
        czas=handler(s)
        if czas == None:
            return { 'segment_status': "ERR", 'segment': s['segment'], 'funkcja': funkcja, 'dlugosc': round(s['dlugosc']), 'debug': "None. Nieobsługiwany return lub dberror dla dlugosci: {}".format(s['dlugosc']) }
        return { "segment_status": "OK", "segment": s['segment'], 'funkcja': funkcja, "dlugosc": round(s['dlugosc']), "czas": round(czas), "nawodniona": self.weze_nawodnione }
# }}}
    def main_process_wariant(self, wariant, data):# {{{
        self.weze_nawodnione=0
        self.weszlismy_oknem=0
        self.sprawilismy_hydrant=0
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
        xj=self.json.read('{}/scenariusz.json'.format(self.zbior))
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
        self.save(udane,nieudane)
# }}}

d=DojazdMW()

# symulacje/office123/sesja1/wyniki.txt
# symulacje/office123/sesja1/scenariusz.json
