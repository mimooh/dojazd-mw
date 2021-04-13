#echo "select * from cnbop"    | sqlite3 -header mw.db
#echo "select * from generics" | sqlite3 -header mw.db 
#echo ".tables"				   | sqlite3 mw.db

# Id | generic | IdDescription                                   | IdIndication | MassClass | Category     | Chassis | Drive | RegistrationNumber | OperationalNumber | VIN               | DevelopmenNumber | AdmissionNumber | PNENMarking         | CrewCapacity | OuterLong | InnerLong | DriveReadyWidth | InnerWidth | OuterOperationalWidth | DriveReadyHeight | InnerHeight | MinSteerLeftWidth | MinSteerRigthWidth | MinTurnBackInnerLeftDiameter | MinTurnBackInnerRightDiameter | MinTurnBackOuterLeftDiameter | MinTurnBackOuterRightDiameter | TangentialWheelRadius | FaceAngle | DescensionAngle | RampAngle | FrontSlack | RearSlack | MMR     | LeftMMROverload | RightMMROverload | MMROverloadFirstAxis | MMROverloadSecondAxis | MMROverloadThirdAxis | FirstAxisHeadroom | SecondAxisHeadroom | ThirdAxisHeadroom | HeadroomBesideAxis | TransverseHeadroomBetweenWheels | MirrorGeometryAbstract     | LadderGeometryAbstract       | LadderLiftParametersId | FirefightingParametersId | ObjectModelFilePath
# 1  | gen1    | Samochód specjalny z podnośnikiem hydraulicznym | PMT 25.D     | Średni    | Miejski      | MAN     | 4x2   | WOT 99VS           | 551 M 53          | WMAN04ZZ97Y183539 | 2006             | n.d             | M-1-3-23/11-0-1     | 3            | 7745.0    | 7520.0    | 2925.0          | 2570.0     | 3670.0                | 3470.0           |             | 5.0               | 5.2                | 7.1                          | 8.0                           | 15.0                         | 15.9                          | 375                   | 14.8      | 13.8            | 18.7      | 2615.0     | 2530.0    | 11940.0 | 5890.0          | 6050.0           | 4475.0               | 7465.0                |                      | 175.0             | 155.0              |                   | 230.0              | 170.0                           | -75;6800;150;100;2000;2300 | 1285;3160;900;6000;3470;3550 | 1                      |                          |
# 2  | gen1    | Ratowniczo-gaśniczy                             | GCBA         | Ciężki    | uterenowiony | SCANIA  | 4x4   | WOT LU86           | 551 M 25          | YS2P4X40002052968 | 2647             | 0080/2008       | S-2-6-5000-8/3200-1 | 6            |           | 8320.0    | 3030.0          | 2625.0     | 3830.0                | 3255.0           | 3250.0      | 5.9               | 5.8                | 10.4                         | 9.2                           | 19.0                         | 18.1                          | 505                   | 26.3      | 17.4            | 17.4      | 1825.0     | 2000.0    | 19525.0 | 7925.0          | 9800.0           | 8395.0               | 11130.0               |                      | 315.0             | 305.0              |                   | 280.0              |                                 | -75;7800;150;100;2000;2300 | 1285;3160;900;6000;3470;3550 |                        |                          |

echo "drop table cnbop" | sqlite3 mw.db 2>/dev/null
echo "drop table generics" | sqlite3 mw.db 2>/dev/null
echo "create table cnbop(id serial primary key , cnbop1 text , cnbop2 text, generic text)" | sqlite3 mw.db
for i in `seq 1 53`; do
	echo "insert into cnbop(cnbop1,cnbop2,generic) values('skręt1', 'wysokość1', 'g1')" | sqlite3 mw.db
done
echo "update cnbop set generic='g2' where id>12;" | sqlite3 mw.db;
echo "update cnbop set generic='g3' where id>23;" | sqlite3 mw.db;
echo "update cnbop set generic='g4' where id>48;" | sqlite3 mw.db;


echo "create table generics(id,kraj,opis,kategoria , pojemnosc_woda , pojemnosc_piana , nom_wyd_autopompy , nom_wyd_motopompy , nom_wyd_autopompy30bar, dod_sr_gasn, nom_zaloga, dzialko_wod_pian, dzialko_wod_pian_przenosne, aparaty_pow, zapasowe_butle, w_110, w_75, w_52, szybkie_natarcie, rozdzielacz_75_110, rozdzielacz_75_52, pradownica_pw_75, pradownica_pw_52, pradownica_pp2, pradownica_pp4, pradownica_pp8, wytwornica_wp2_75, wytwornica_wp4_75, stojak_hydrant, drabina_wysuw_2p, drabina_slup, drabina_nasad, wentylator, kosz_rat, pion_wodny, duszczyk, zwijadlo, noszaki_75, noszaki_52, noszaki_38, noszaki_42, harmonijka_w_75, harmonijka_w_52, petla_w_52, petla_w_38, petla_w_42)" | sqlite3 mw.db
echo "insert into generics(id,kraj,opis) values

('gen1' , 'pl' , 'standard wyposażenia typoszeregu GBA 2/16'   ) ,
('gen2' , 'pl' , 'standard wyposażenia typoszeregu GCBA 4/24'  ) ,
('gen3' , 'pl' , 'standard wyposażenia typoszeregu GCBA 7/40'  ) ,
('gen4' , 'pl' , 'standard wyposażenia typoszeregu GCBA 11/60' ) ,
('gen5' , 'pl' , 'standard wyposażenia typoszeregu SD'         ) ,
('gen6' , 'pl' , 'standard wyposażenia typoszeregu SH'         ) ,
('gen7' , 'de' , 'modyfikacja pojazdy europejskie'             ) ,
('gen8' , 'en' , 'modyfikacja pojazdy anglosaskie'             )

;
" | sqlite3 mw.db

