#
# En impementering av trapesmetoden for å integrere
#

def TrapesMetoden(f, a, b, N = 100000):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Antall trapeser

    # Bredden per trapes
    dx = (b - a) / N
    # Arealet under grafen
    A = (f(a) + f(b)) / 2

    # Loop gjennom alle trapesene
    for i in range(1, N):
        # Legg sammen høyden i rektanglene
        A += f(a + i * dx)

    # Multipliser med bredden
    A *= dx

    # returner arealet under grafen f
    return A
