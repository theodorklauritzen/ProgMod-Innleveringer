# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 09:21:34 2020

@author: xuper
"""

from pylab import *

k = 0.1         # En konstant som forteller hvor raske temperaturen endrer seg
T_O = 21        # Omgivelsestemperaturen (C)
T_0 = 75        # Start temperaturen (C)
t_S = 60        # Slutttid (min)

N = 10000       # Antal interasjoner
dt = (t_S) / N  # Tidssteg

# Arayer
tid = zeros(N)  # Tid (min)
T   = zeros(N)  # Termperatur (C)

# Initsialbetingelser
T[0] = T_0

# Eulers metode
for i in range(N - 1):
    tid[i + 1] = tid[i] + dt
    T[i + 1] = T[i] - k * (T[i] - T_O) * dt

# Plot resultatet
plot(tid, T)

title("Temperaturen i kaffekoppen")
xlabel("Tid (min)")
ylabel("Temperatur (C)")

show()