#
# En impementering av Simpsons metode for å integrere
#

def SimpsonsMetode(f, a, b, N = 100000):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Antall søyler

    # Bredden per søyle
    h = (b - a) / (2 * N)
    # Arealet under grafen
    A = f(a) + 4 * f(a + h) + f(b)

    for i in range(1, N):
        A += 2 * f(a + i * 2 * h) + 4 * f(a + (i * 2 + 1) * h)

    # Multipliser med h / 3
    A *= h / 3

    # returner arealet under grafen f
    return A
