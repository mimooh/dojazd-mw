#echo "drop table Generics" | sqlite3 firetrucks.db 2>/dev/null
#echo "create table Generics(id ,kraj,opis,kategoria , pojemnosc_woda , pojemnosc_piana , nom_wyd_autopompy , nom_wyd_motopompy , nom_wyd_autopompy30bar, dod_sr_gasn, nom_zaloga, dzialko_wod_pian, dzialko_wod_pian_przenosne, aparaty_pow, zapasowe_butle, w_110, w_75, w_52, szybkie_natarcie, rozdzielacz_75_110, rozdzielacz_75_52, pradownica_pw_75, pradownica_pw_52, pradownica_pp2, pradownica_pp4, pradownica_pp8, wytwornica_wp2_75, wytwornica_wp4_75, stojak_hydrant, drabina_wysuw_2p, drabina_slup, drabina_nasad, wentylator, kosz_rat, pion_wodny, duszczyk, zwijadlo, noszaki_75, noszaki_52, noszaki_38, noszaki_42, harmonijka_w_75, harmonijka_w_52, petla_w_52, petla_w_38, petla_w_42)" | sqlite3 firetrucks.db
#echo "drop table FireTrucks" | sqlite3 firetrucks.db 2>/dev/null
#echo "create table FireTrucks(Id,generic,IdDescription,IdIndication,MassClass,Category,Chassis,Drive,RegistrationNumber,OperationalNumber,VIN,DevelopmentNumber,AdmissionNumber,PNENMarking,CrewCapacity,OuterLong,InnerLong,DriveReadyWidth,InnerWidth,OuterOperationalWidth,DriveReadyHeight,InnerHeight,MinSteerLeftWidth,MinSteerRigthWidth,MinTurnBackInnerLeftDiameter,MinTurnBackInnerRightDiameter,MinTurnBackOuterLeftDiameter,MinTurnBackOuterRightDiameter,TangentialWheelRadius,FaceAngle,DescensionAngle,RampAngleA,RampAngleB,RampAngleH,RampAngle,FrontSlack,RearSlack,MMR,LeftMMROverload,RightMMROverload,MMROverloadFirstAxis,MMROverloadSecondAxis,MMROverloadThirdAxis,FirstAxisHeadroom,SecondAxisHeadroom,ThirdAxisHeadroom,HeadroomBesideAxis,TransverseHeadroomBetweenWheels,MirrorGeometryAbstract,LadderGeometryAbstract,LadderLiftParametersId,FirefightingParametersId,ObjectModelFilePath)" | sqlite3 firetrucks.db

echo "delete from Generics" | sqlite3 firetrucks.db
cat csv/generyki.csv | grep -v '^id' | sqlite3 -csv firetrucks.db ".import /dev/stdin Generics"
echo "select * from Generics" | sqlite3 -header firetrucks.db

# echo "delete from FireTrucks" | sqlite3 firetrucks.db
# cat csv/firetrucks.csv | sqlite3 -csv firetrucks.db ".import /dev/stdin FireTrucks"
# echo "select * from FireTrucks" | sqlite3 -header firetrucks.db
