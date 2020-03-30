#
# En impementering av Monte Carlo metoden for å integrere
#

import random

def MonteCarlo(f, a, b, N = 100000, randomAlgorithm = random.random):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Antall punkter
    # randomAlgorithm : En algoritme som gir tilfeldige tall

    # Lengden på intervallet
    w = (b - a)

    # En variabel for å lagre summen av høyden
    sum = 0

    # En loop for kjører N ganger
    for i in range(N):
        # Regn ut en tilfeldig x verdi i intervallet
        x = randomAlgorithm() * w + a
        # Legg til funksjonsverdien til f i punktet x til summen
        sum += f(x)

    # Finn den gjnnomsnittlige høyden og multipliser den med bredden av integralet
    return sum / N * w
