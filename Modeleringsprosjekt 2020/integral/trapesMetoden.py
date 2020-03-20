#
# En impementering av trapesmetoden for å integrere
#

def TrapesMetoden(f, a, b, N = 100000):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Antall trapeser

    # Bredden per rektangel
    dx = (b - a) / N
    # Arealet under grafen
    A = f(a) / 2

    # Loop gjennom alle trapesene
    for i in range(1, N):
        # Legg sammen høyden i rektanglene
        A += f(a + i * dx)

    A += f(b) / 2
    # Multipliser med bredden
    A *= dx

    # returner arealet under grafen f
    return A

"""
NOTE:
Her er mye av koden effektivisert!!

FØR:
A = 0
Loopen fra og med 0 til N
    A += (f(a + i * dx) + f(a + (i + 1) * dx)) * dx / 2

return A

TANKEGANG:
Dette kan kortes ned ved å tenke at man kan multipliserre med dx / 2 i slutten siden dette er en konstant

Så kan vi tenke oss at vi regner nå ut hoyden i hvert punkt 2 ganger, det er unødvendig.
    Dette gjelder ikke i punktene x = a og x = b.  Her skal vi bare regne ut høyden 1 gang.
Derfor kan vi starte med å legge til høyden i x = a, altså A = f(a)
Så kan vi gå gjennom alle hoydene i trapesene og legge dem til * 2
Så må vi huske å ha med den siste høyden i x = b.
Så denne legger vi til slutt.

Helt til slutt så ganger vi med dx / 2.
Men det er ikke vits å dele på 2, hvis vi heller ikke ganger med 2.  Da sparer vi en operasjon.
Så da må verdiene i x = a og x = b, bare deles på to så er vi der.  Da blir koden som vist over

"""
