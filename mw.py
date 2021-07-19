import json
from collections import OrderedDict
from include import Json
from include import Dump as dd

# jezeli start=1 to wygneruj nowy plik symulacja_data.godzina.txt
# wykluczenie ze wzgledu na: a) przekroczenie sumy wezy
# wypełnić funkcje

class DojazdMW:

    def __init__(self):# {{{
        self.json=Json()
        self.make_segments_map()
        self.make_db_czynnosci()
        self.make_db_drabiny()
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
            't_sprawianie_hydrantu_podziemnego'                     : 70,
            't_sprawianie_hydrantu_naziemnego'                      : 30,
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
            't_przejazd_roty_dźwigiem'                              : 60,
            'v_nie_gaśnicza_wewn_poziom_dym0'                       : 1.33,
            'v_zewn'                                                : 2,
            'v_nie_gaśnicza_wewn_pion_dym0'                         : OrderedDict([(12,100), (25,220), (55,1060)]),
            't_wyważanie_drzwi_drewniane_dym0'                      : 80,
            't_wyważanie_drzwi_drewniane_dym1'                      : 170,
            't_wyważanie_drzwi_antywłamaniowe_dym0'                 : 450,
            't_wyważanie_drzwi_antywłamaniowe_dym1'                 : 740,

        }

# }}}
    def make_db_drabiny(self):# {{{
        # składniki czasu: 
        # 1. zdjęcie drabiny (wart. stała): 60s
        # 2. podróż z drabiną (1.36 m/s): 30s dla 20m
        # 3. drabinę spraw: 190
        # 4. wejście po drabinie

        # logika typu: jezeli segment wynosi 10m to czas wynosi 35
        # 280: 80 biegu + 200 drabinę spraw
        self.db_drabiny={
            "drabina_przystawna":         { '10': 20 },
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

    def wewn_dym0_poziom(self, segment):# {{{
        # z wariantu wynika czy idą z wężami
        dd(segment)
        t=segment['długość'] * self.query("v_linia_gaśn_w52_wewn_poziom_dym0_kregi", segment['długość'])
        dd(t)
# }}}
    def wewn_dym0_pion(self, segment):# {{{
        # z wariantu wynika czy idą z wężami
        dd(segment)
# }}}
    def wewn_dym0_dzwig(self, segment):# {{{
        # Przejazd dźwigiem wzgledem danej konfiguracji pieter
        dd(segment)
# }}}
    def wewn_dym0_hydrant(self, segment):# {{{
        ''' Od Marcina czas na podłączenie hydrantu'''
        dd(25)
        
# }}}
    def wewn_dym1_poziom(self, segment):# {{{
        dd(segment)
# }}}
    def wewn_dym1_pion(self, segment):# {{{
        dd(segment)
# }}}
    def wewn_dym1_dzwig(self, segment):# {{{
        dd(segment)
# }}}
    def wewn_dym1_hydrant(self, segment):# {{{
        dd(segment)
# }}}
    def zewn_poziom(self, segment):# {{{
        dd(segment)
# }}}
    def zewn_drabina_przystawna(self, segment):# {{{
        dd(segment)
# }}}
    def zewn_drabina_mechaniczna(self, segment):# {{{
        dd(segment)
# }}}
    def main(self):# {{{
        self.warianty=self.json.read('scenariusz.json')['warianty'] 
        self.scenariusz=self.json.read('scenariusz.json')['conf']
        for scenariusz,segmenty in self.warianty.items():
            print("WARIANT")
            for s in segmenty['segmenty']:
                handler=getattr(self, self.segments_map[s['segment']])
                s['segment_name']=self.segments_map[s['segment']]
                s['segment_code']=scenariusz
                handler(s)
                dd("=======")
# }}}

d=DojazdMW()
