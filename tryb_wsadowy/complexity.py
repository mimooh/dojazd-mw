x1=100 # miejsc pozarow
x2=3 # maly duzy sredni
x3=10 # rozstawien samochodow na linii
x4=3 # zestawow samochodow: gba vs gba+drabina
x5=3 # wyposazen samochodow: 100m węży vs 20m węży vs D10W vs noszaki itd.

scenariuszy=x1*x2*x3*x4*x5
wariantow=5 # pathfindingów

print("scenariuszy:", scenariuszy)
print("godzin na wygenerowanie i przekazanie wariantów do MW (szacunkowy koszt 1 sekunda):", scenariuszy*wariantow/3600)


