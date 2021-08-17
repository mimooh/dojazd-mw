
x1=100  # miejsc pozarow
x2=3    # maly duzy sredni 
x3=10   # rozstawien samochodow na linii
x4=3    # zestawow samochodow: gba vs gba+drabina
x5=1    # wyposazen samochodow: 100m wezy vs 20m wezy vs D10W vs noszaki itd.
x6=1    # zmiennosc zalogi (monte carlo)

scenariuszy=x1*x2*x3*x4*x5*x6
czas_generowania_scenariusza=30 # sekund

print("scenariuszy:", scenariuszy)
print("godzin na wygenerowanie i przekazanie wariantow do MW:", scenariuszy*czas_generowania_scenariusza/(3600*24), "dni")


