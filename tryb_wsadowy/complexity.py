
x1=100  # miejsc pozarow
x2=3    # maly duzy sredni 
x3=10   # rozstawień samochodów na linii
x4=3    # zestawów samochodów: gba vs gba+drabina
x5=1    # wyposażeń samochodów: 100m węży vs 20m węży vs D10W vs noszaki itd.
x6=1    # zmienność załogi (monte carlo)

scenariuszy=x1*x2*x3*x4*x5*x6
czas_generowania_scenariusza=30 # sekund

print("scenariuszy:", scenariuszy)
print("godzin na wygenerowanie i przekazanie wariantów do MW:", scenariuszy*czas_generowania_scenariusza/(3600*24), "dni")


