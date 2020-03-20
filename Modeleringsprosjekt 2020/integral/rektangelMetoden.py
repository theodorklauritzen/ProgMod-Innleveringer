#
# En impementering av rektangelmetoden for å integrere
#

def RektangelMetoden(f, a, b, N = 100000):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Antall rektangler

    # Bredden per rektangel
    dx = (b - a) / N
    # Arealet under grafen
    A = 0

    # Loop gjennom alle rekangelene
    for i in range(N):
        # Legg sammen høyden i rektanglene
        A += f(a + i * dx)

    # Multipliser med bredden per integral for å finne arealet
    A *= dx

    # returner arealet under grafen f
    return A
