# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 08:20:13 2020

@author: Theodor 2G
"""

Regresjon_intervall_slutt = 90

# En fuksjon som regner ut løsligheten (mg/L) til NH_3 gitt en temperatur T (C)
def L_NH_3(T):
    return 0.00868 * T ** 2 - 1.66 * T + 87.4

# En fuksjon som regner ut løsligheten (mg/L) til NaCl gitt en temperatur T (C)
def L_NaCl(T):
    return 0.000295 * T ** 2 - 0.00554 * T + 35.7

# En likning som er differansen mellom løsningen til NH_3 og NaCl
def l(T):
    return L_NH_3(T) - L_NaCl(T)

# halveringsmetoden
def halvvering(f, a, b, tol = 1e-7):
    # f : en funksjon å finne nullpunkter til
    # a : Starten av et intervall
    # b : Slutten av et intervall
    # tol : Toleransen på hvor nærme 0 man kan være
    
    # Returner None hvis det ikke er noen nullpunkter
    if f(a) * f(b) > 0:
        return None
    
    # Returner a hvis a er et nullpunkt
    if f(a) == 0:
        return a
    
    # Returner b hvis b er et nullpunkt
    if f(b) == 0:
        return b
    
    # Loop til vi finner et svar, men ikke mer enn 10000 ganger
    for i in range(10000):
        # Regn ut midtpunktet
        m = (a + b) / 2 
        
        # Sjekk om midtpunktet er nærme nok 0
        if abs(f(m)) < tol:
            return m
        
        # Finn ut om nullpunktet er mellom a og m, eller m og b
        if f(a) * f(m) < 0:
            b = m
        elif f(m) * f(b) < 0:
            a = m
    
    # Returner None hvis vi har satt oss fast og loopen har kjørt 10000 ganger
    return None

# Lag en tom liste der vi kan fylle inn nullpunkter
nullpunkter = []

# Let etter nullpunkter i små intervaller i det store intervallet
for i in range(Regresjon_intervall_slutt - 1):
    # Finn eventuelle nullpunkter
    nullpunkt = halvvering(l, i, i + 1)
    
    # Hvis vi fant et nullpunkt, legg det til i lista
    if not (nullpunkt is None):
        nullpunkter.append(nullpunkt)

# Print svaret
# Det var bare ett nullpunkt så da kan jeg skrive nullpunkter[0]
print("Løsligheten er lik når Temperaturen er {}".format(nullpunkter[0]))