import json
from collections import OrderedDict
from include import Json
from include import Dump as dd

class DojazdMW:
    def __init__(self):# {{{
        self.json=Json()
        self.make_db()
        #self.read_input()
# }}}
    def query(self, param, droga):# {{{
        if isinstance(self.db[param], dict):
            for t in list(self.db[param].keys()):
                if t >= droga:
                    return self.db[param][t]
        else:
            return self.db[param]

# }}}
    def make_db(self):# {{{
        self.db={
            't_sprawianie_hydrantu_podziemnego'               : 70,
            't_sprawianie_hydrantu_naziemnego'                : 30,
            't_zasilenie_samochodu'                           : OrderedDict([(20,30)]),
            't_zasilenie_instalacji_w75x1'                    : OrderedDict([(20,70)]),
            't_zasilenie_instalacji_w75x2'                    : OrderedDict([(20,100)]),
            't_sprawianie_motopompy_MP81_z_linia_w75'         : OrderedDict([(20,320)]),
            't_sprawianie_motopompy_szlam_z_linia_w75'        : OrderedDict([(20,510)]),
            't_sprawianie_zbiornika_2i5m3'                    : 290,
            't_sprawianie_zbiornika_5m3'                      : 150,
            't_linia_główna_w75_do_rozdzielacza'              : 30,
            't_linia_główna_w75x2_do_rozdzielacza_harmonijka' : 15,
            't_przygotowanie_roty_gaśn'                       : 50,
            'v_rota_gaśn_zewn_poziom_dym0'                    : 1,
            'v_rota_gaśn_wewn_poziom_dym0'                    : 0.8,
            'v_rota_gaśn_wewn_poziom_dym1'                    : 0.38,
            't_rota_gaśn_wewn_pion_dym0'                      : OrderedDict([(12,100),(25,330),(55,1026)]),
            't_rota_gaśn_wewn_pion_dym1'                      : OrderedDict([(12,140),(25,500),(55,1520)]),

            'v_linia_gaśn_w52_wewn_poziom_dym1_kregi'         : 0.25,
            't_linia_gaśn_w52_wewn_pion_dym1_kregi_1rota'     : OrderedDict([(12,620),(25,1120),(55,2120)]),
            't_linia_gaśn_w52_wewn_pion_dym1_kregi_2roty'     : OrderedDict([(12,500),(25,1060),(55,1520)]),
            'v_linia_gaśn_w52_wewn_poziom_dym0_kregi'         : 0.8,
            't_linia_gaśn_w52_wewn_pion_dym0_kregi_1rota'     : OrderedDict([(12,230),(25,760),(55,1700)]),
            't_linia_gaśn_w52_wewn_pion_dym0_kregi_2roty'     : OrderedDict([(12,170),(25,700),(55,1520)]),

            'v_linia_gaśn_w42_wewn_poziom_dym1_kregi'         : 0.26,
            't_linia_gaśn_w42_wewn_pion_dym1_kregi_1rota'     : OrderedDict([(12,620),(25,1120),(55,2120)]),
            't_linia_gaśn_w42_wewn_pion_dym1_kregi_2roty'     : OrderedDict([(12,500),(25,1060),(55,1520)]),
            'v_linia_gaśn_w42_wewn_poziom_dym0_kregi'         : 1,
            't_linia_gaśn_w42_wewn_pion_dym0_kregi_1rota'     : OrderedDict([(12,230),(25,760),(55,1700)]),
            't_linia_gaśn_w42_wewn_pion_dym0_kregi_2roty'     : OrderedDict([(12,170),(25,700),(55,1520)]),

            'v_linia_gaśn_w52_wewn_poziom_dym1_kasetony'      : 0.4,
            't_linia_gaśn_w52_wewn_pion_dym1_kasetony_1rota'  : OrderedDict([(12,560),(25,1000),(55,1940)]),
            't_linia_gaśn_w52_wewn_pion_dym1_kasetony_2roty'  : OrderedDict([(12,320),(25,880),(55,1510)]),
            'v_linia_gaśn_w52_wewn_poziom_dym0_kasetony'      : 1,
            't_linia_gaśn_w52_wewn_pion_dym0_kasetony_1rota'  : OrderedDict([(12,500),(25,940),(55,1880)]),
            't_linia_gaśn_w52_wewn_pion_dym0_kasetony_2roty'  : OrderedDict([(12,320),(25,700),(55,1510)]),

            'v_linia_gaśn_w42_wewn_poziom_dym1_kasetony'      : 0.4,
            't_linia_gaśn_w42_wewn_pion_dym1_kasetony_1rota'  : OrderedDict([(12,500),(25,940),(55,1940)]),
            't_linia_gaśn_w42_wewn_pion_dym1_kasetony_2roty'  : OrderedDict([(12,320),(25,880),(55,1510)]),
            'v_linia_gaśn_w42_wewn_poziom_dym0_kasetony'      : 1.33,
            't_linia_gaśn_w42_wewn_pion_dym0_kasetony_1rota'  : OrderedDict([(12,500),(25,940),(55,1880)]),
            't_linia_gaśn_w42_wewn_pion_dym0_kasetony_2roty'  : OrderedDict([(12,320),(25,700),(55,1510)]),

            't_linia_gaśn_w52_wewn_pion_dym1_dusza_klatki_2roty'  : OrderedDict([(12,500),(25,940),(55,1940)]),
            't_linia_gaśn_w52_wewn_pion_dym1_dusza_klatki_3roty'  : OrderedDict([(12,320),(25,880),(55,1510)]),
            't_linia_gaśn_w52_wewn_pion_dym0_dusza_klatki_2roty'  : OrderedDict([(12,500),(25,940),(55,1880)]),
            't_linia_gaśn_w52_wewn_pion_dym0_dusza_klatki_3roty'  : OrderedDict([(12,320),(25,700),(55,1510)]),

            't_linia_gaśn_w42_wewn_pion_dym1_dusza_klatki_2roty'  : OrderedDict([(12,500),(25,940),(55,1940)]),
            't_linia_gaśn_w42_wewn_pion_dym1_dusza_klatki_3roty'  : OrderedDict([(12,320),(25,880),(55,1510)]),
            't_linia_gaśn_w42_wewn_pion_dym0_dusza_klatki_2roty'  : OrderedDict([(12,440),(25,940),(55,1880)]),
            't_linia_gaśn_w42_wewn_pion_dym0_dusza_klatki_3roty'  : OrderedDict([(12,320),(25,700),(55,1510)]),

            't_szybkie_natarcie_zewn_poziom'        : OrderedDict( [(20,50)]),
            't_szybkie_natarcie_zewn_pion_elewacja' : OrderedDict( [(12,190)]),

            't_linia_gaśn_w52_elewacja'  : OrderedDict([(12,440),(25,880),(55,2120)]),
            't_linia_gaśn_w42_elewacja'  : OrderedDict([(12,430),(25,860),(55,1880)]),
        }

# }}}
    def read_input(self):# {{{
        f=self.json.read('input.json') 
        for i in f:
            print(i, i['scenariusz'])
# }}}

d=DojazdMW()
print(d.query("v_linia_gaśn_w42_wewn_poziom_dym0_kasetony", 7))

