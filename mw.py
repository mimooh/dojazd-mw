import json
from collections import OrderedDict
from include import Json
from include import Dump as dd

class DojazdMW:
    def __init__(self):# {{{
        self.json=Json()
        self.make_db()
        self.read_input()
# }}}
    def query(self, param, droga):# {{{
        for t in list(self.db[param].keys()):
            if t >= droga:
                return self.db[param][t]
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
print(d.query('t_linia_gaśn_w42_elewacja', 5))


'''
# {{{
TODO
Nazwa                   ; Opis                                                                                                                                                                            ; Liczba rot ; Czas 
Sprawianie drabiny      ; sprawienie drabiny przystawnej typu DW10 (max. wysuw) i budowa stanowiska gaśniczego na drabinie w odległości do 20 m od pojazdu pożarniczego                                   ; 2          ; 260            
Sprawianie drabiny      ; sprawienie drabiny przystawnej nasadkowej (z 4 przeseł) i budowa stanowiska gaśniczego na drabinie w odległości do 20 m od pojazdu pożarniczego                                 ; 2          ; 280            
Sprawianie drabiny      ; sprawienie drabiny mechanicznej do kondygnacji na wys. do 12 m z dwoma ratownikami w koszu drabiny przygotowanych do podania prądu gaśniczego z działka wodno-pianowego         ; 2          ; 160            
Sprawianie drabiny      ; sprawienie drabiny mechanicznej do kondygnacji na wys. do 25 m z dwoma ratownikami w koszu drabiny przygotowanych do podania prądu gaśniczego z działka wodno-pianowego         ; 2          ; 180            
Sprawianie drabiny      ; sprawienie drabiny mechanicznej do kondygnacji na wys. do 55 m z dwoma ratownikami w koszu drabiny przygotowanych do podania prądu gaśniczego z działka wodno-pianowego         ; 2          ; 400            
Sprawianie podnośnika   ; sprawienie podnośnika hydraulicznego do kondygnacji na wys. do 12 m z dwoma ratownikami w koszu podnośnika przygotowanych do podania prądu gaśniczego z działka wodno-pianowego ; 2          ; 250            
Sprawianie podnośnika   ; sprawienie podnośnika hydraulicznego do kondygnacji na wys. do 25 m z dwoma ratownikami w koszu podnośnika przygotowanych do podania prądu gaśniczego z działka wodno-pianowego ; 2          ; 290            
Sprawianie podnośnika   ; sprawienie podnośnika hydraulicznego do kondygnacji na wys. do 55 m z dwoma ratownikami w koszu podnośnika przygotowanych do podania prądu gaśniczego z działka wodno-pianowego ; 2          ; 490            
Sprawianie drabiny      ; sprawienie drabiny przystawnej typu DW10 (max. wysuw) i budowa stanowiska gaśniczego na drabinie w odległości do 20 m od pojazdu pożarniczego                                   ; 2          ; 260            
Sprawianie drabiny      ; sprawienie drabiny przystawnej nasadkowej (z 4 przeseł) i budowa stanowiska gaśniczego na drabinie w odległości do 20 m od pojazdu pożarniczego                                 ; 2          ; 280            
Sprawianie sprzętu      ; przygotowanie sprzętu do prowadzenia wentylacji taktycznej w odległości 20 m od pojazdu pożarniczego                                                                            ; 1          ; 120            
Przygotowania           ; przygotowanie roty do wejścia w strefę zagrożenia i podjęcia działań ratowniczych (rota w gotowości przy samochodzie)                                                           ; 1          ; 25             
Przygotowania           ; przygotowanie medycznego pola sprzętowego/strefy udzielania KPP                                                                                                                 ; 1          ; 70             
Przygotowania           ; uruchomienie systemu monitorowania pracy w sprzęcie ochrony układu oddechowego                                                                                                  ; 1          ; 30             
Zabezpieczanie terenu   ; zabezpieczenie terenu działań ratowniczych pachołkami, wygrodzenie terenu taśmą ostrzegawczą                                                                                    ; 1          ; 170            
Rozpoznanie             ; przeprowadzenie rozpoznania wstępnego (tzw. 3600 dot. budynków wolnostojących np. jednorodzinnych), wyznaczenie strefy zagrożenia                                               ; 1          ; 70             
Sprawienie drabiny      ; sprawienie drabiny przystawnej typu DW10 do asekuracyji działań ratowniczych w odległości do 20 m od pojazdu pożarniczego                                                       ; 2          ; 210            
Sprawienie drabiny      ; sprawienie drabiny przystawnej nasadkowej  (z czterech przęseł) do asekuracyji działań ratowniczych w odległości do 20 m od pojazdu pożarniczego                                ; 2          ; 230            
Sprawienie drabiny      ; sprawienie drabiny mechanicznej do kondygnacji na wys. do 12 m celem asekuracji działań ratowniczych.                                                                           ; 1          ; 140            
Sprawienie drabiny      ; sprawienie drabiny mechanicznej do kondygnacji na wys. do 25 m celem asekuracji działań ratowniczych.                                                                           ; 1          ; 160            
Sprawienie drabiny      ; sprawienie drabiny mechanicznej do kondygnacji na wys. do 55 m celem asekuracji działań ratowniczych.                                                                           ; 1          ; 380            
Sprawienie drabiny      ; sprawienie podnośnika hydraulicznego do kondygnacji na wys. do 12 m celem asekuracji działań ratowniczych                                                                       ; 1          ; 230            
Sprawienie drabiny      ; sprawienie podnośnika hydraulicznego do kondygnacji na wys. do 25 m celem asekuracji działań ratowniczych                                                                       ; 1          ; 260            
Sprawienie drabiny      ; sprawienie podnośnika hydraulicznego do kondygnacji na wys. do 55 m celem asekuracji działań ratowniczych                                                                       ; 1          ; 460            
Sprawienie drabiny      ; sprawienie skokochronu w odległości do 20 m od pojazdu pożarniczego                                                                                                             ; 1          ; 130            
Sprawienie drabiny      ; sprawienie drabiny przystawnej typu DW10 do asekuracyji działań ratowniczych w odległości do 20 m od pojazdu pożarniczego                                                       ; 4          ; 200            
Sprawienie drabiny      ; sprawienie drabiny przystawnej nasadkowej  (z czterech przęseł) do asekuracyji działań ratowniczych w odległości do 20 m od pojazdu pożarniczego                                ; 2          ; 240            
Sprawienie skokochronu  ; sprawienie skokochronu w odległości do 20 m od pojazdu pożarniczego                                                                                                             ; 1          ; 150            
Przygotownie asekuracji ; przygotowanie roty asekuracyjnej do działań w strefie zagrożenia wraz z linią asekuracyjną tzw. Rotę RIT                                                                        ; 1          ; 110            
Przejście wewnętrzne    ; dotarcie do dźwigu dla ekip ratowniczych roty wyposażonej w sprzęt do tzw. rozpoznania bojem, do 20 m w drodze poziomej                                                         ; 1          ; 10             
Przejazd dźwigiem       ; przejazd dźwigiem dla ekip ratowniczych do najwyższej kondygnacji wg. PN-EN 81-72                                                                                               ; 1          ; 60             
Przejście wewnętrzne    ; poruszanie się roty ratowniczej wewnątrz budynku (bez linii gaśniczej) w drogach poziomych, praca bez zadymienia, każde 20 m drogi                                              ; 1          ; 15             
Przejście wewnętrzne    ; poruszanie się roty ratowniczej wewnątrz budynku (bez linii gaśniczej) w drogach pionowych, praca bez zadymienia, na wysokość do 12 m wysokości budynku                         ; 1          ; 100            
Przejście wewnętrzne    ; poruszanie się roty ratowniczej wewnątrz budynku (bez linii gaśniczej) w drogach pionowych, praca bez zadymienia, na wysokość do 25 m wysokości budynku                         ; 1          ; 220            
Przejście wewnętrzne    ; poruszanie się roty ratowniczej wewnątrz budynku (bez linii gaśniczej) w drogach pionowych, praca bez zadymienia, na wysokość do 55 m wysokości budynku                         ; 1          ; 1060           
Pokonywanie przeszkody  ; wyważenie drzwi drewnianych praca bez zadymienia                                                                                                                                ; 1          ; 80             
Pokonywanie przeszkody  ; wyważenie drzwi antywłamaniowych praca bez zadymienia                                                                                                                           ; 1          ; 450            
Pokonywanie przeszkody  ; wyważenie drzwi drewnianych, praca w zadymieniu                                                                                                                                 ; 1          ; 170            
Pokonywanie przeszkody  ; wyważenie drzwi antywłamaniowych praca w zadymieniu                                                                                                                             ; 2          ; 740            
Przejście zewnętrzne    ; poruszanie się roty ratowniczej na zewnątrz budynku, każde 20 m drogi                                                                                                           ; 2          ; 10             
Sprawienie drabiny      ; sprawienie drabiny przystawnej typu DW10 o max. wysuwie  w odległości do 20 m od pojazdu pożarniczego i wejście ratownika przez otwór okienny                                   ; 2          ; 230            
Sprawienie drabiny      ; sprawienie drabiny przystawnej nasadkowej  (z czterech przęseł) w odległości do 20 m od pojazdu pożarniczego i wejście ratownika przez otwór okienny                            ; 2          ; 250            
# }}}
'''
