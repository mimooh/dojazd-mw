#echo "select * from cnbop"    | sqlite3 -header mw.db
#echo "select * from generics" | sqlite3 -header mw.db 
#echo ".tables"				   | sqlite3 mw.db

echo "drop table cnbop" | sqlite3 mw.db 2>/dev/null
echo "drop table generics" | sqlite3 mw.db 2>/dev/null
echo "create table cnbop(id serial primary key , cnbop1 text , cnbop2 text, generic text)" | sqlite3 mw.db
for i in `seq 1 53`; do
	echo "insert into cnbop(cnbop1,cnbop2,generic) values('skręt1', 'wysokość1', 'g1')" | sqlite3 mw.db
done
echo "update cnbop set generic='g2' where id>12;" | sqlite3 mw.db;
echo "update cnbop set generic='g3' where id>23;" | sqlite3 mw.db;
echo "update cnbop set generic='g4' where id>48;" | sqlite3 mw.db;


echo "create table generics(id,opis,kategoria , pojemnosc_woda , pojemnosc_piana , nom_wyd_autopompy , nom_wyd_motopompy , nom_wyd_autopompy30bar, dod_sr_gasn, nom_zaloga, dzialko_wod_pian, dzialko_wod_pian_przenosne, aparaty_pow, zapasowe_butle, w_110, w_75, w_52, szybkie_natarcie, rozdzielacz_75_110, rozdzielacz_75_52, pradownica_pw_75, pradownica_pw_52, pradownica_pp2, pradownica_pp4, pradownica_pp8, wytwornica_wp2_75, wytwornica_wp4_75, stojak_hydrant, drabina_wysuw_2p, drabina_slup, drabina_nasad, wentylator, kosz_rat, pion_wodny, duszczyk, zwijadlo, noszaki_75, noszaki_52, noszaki_38, noszaki_42, harmonijka_w_75, harmonijka_w_52, petla_w_52, petla_w_38, petla_w_42)" | sqlite3 mw.db
echo "insert into generics(id,opis) values

('gen1'    , 'standard wyposażenia typoszeregu GBA 2/16'   ),
('gen2'    , 'standard wyposażenia typoszeregu GCBA 4/24'  ),
('gen3'    , 'standard wyposażenia typoszeregu GCBA 7/40'  ),
('gen4'    , 'standard wyposażenia typoszeregu GCBA 11/60' ),
('gen5'    , 'standard wyposażenia typoszeregu SD'         ),
('gen6'    , 'standard wyposażenia typoszeregu SH'         ),
('gen_eur' , 'modyfikacja pojazdy europejskie'             ),
('gen_usa' , 'modyfikacja pojazdy anglosaskie'             )

;
" | sqlite3 mw.db

