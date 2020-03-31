#
# En impementering av Gauss Kvadratur for å integrere
#

from numpy.polynomial import polynomial as P

# Denne funksjonene returnerer Legendre polynomene
def legendrePolynom(n):
    # n : graden til Legendre polynomet

    # Rekursiv formel: https://en.wikipedia.org/wiki/Legendre_polynomials#Definition_via_generating_function
    # (n + 1) P_{n + 1}(x) = (2n + 1)xP_n(x) - n P_{n - 1}(x)

    # Dette er initsialbetingelsene til den rekursive formelen
    if n == 0:
        return [1]

    if n == 1:
        return [0, 1]

    # Så bruker vi den rekursive formelen videre
    # n P_n(x) = (2n - 1)xP_{n - 1}(x) - (n - 1) P_{n - 2}(x)

    ret = P.polymul([0, 2 * n - 1], legendrePolynom(n - 1))
    ret = P.polyadd(ret, P.polymul(legendrePolynom(n - 2), [1 - n]))
    ret = P.polymul(ret, [1 / n])

    # Returner resultatet
    return ret

# En funksjon som finner en vekt til en x verdi
def vekt(polyDer, x):
    # polyDer : Den deriverte til et legendre polynom
    # x : x å finne vekten til

    # w_i = 2 / ((1 - x_i^2) * (P_n'(x_i))^2 )

    return 2 / ((1 - x ** 2)  * (P.polyval(x, polyDer) ** 2))

# En fuksjon som returerer en annen funksjon for å skise integralet mellom a og b til integralet mellom -1 og 1
def endreIntervall(f, a, b):
    # f : en funksjon
    # a : starten på et intervall
    # b : slutten på et intervall

    # En funksjon å returnere
    def ret(x):
        # x : en verdi å regne ut den tilsvarende verdien til

        return (b - a) / 2 * f((b - a) / 2 * x + (a + b) / 2)

    # Returner funksjonen
    return ret

# En funksjon som bruker Gauss kvadrartur til å regne ut det bestemte integralet til en funksjon
def GaussKvadratur(f, a = -1, b = 1, N = 7):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Hvilken grad vi skal ha av polynomet

    # Sjekk at N er et oddetall større enn 0, årsaken er at vi må ha et partall antall ukjente i likningen
    # For eksemper hvis N = 1, er integralet det samme som w_1 * f(x_1) + w_2 * f(x_2), altså 4 ukjente
    if N % 2 == 0 or N < 1:
        # Kast en feil hvis N er spesiefisert feil
        raise ValueError("N må være et oddetall større enn 0")

    # Regn ut legendre graden til den tilsvarende graden av polynomet som ble spesifisert
    n = int((N + 1) / 2)

    # Skvis funksjonen ned så a blir liggende på -1 og b på 1.
    nyF = endreIntervall(f, a, b)

    # IDEA: Mye kan lagres i en slags cache, for å effektivisere, men da kommer ikke metoden så godt fram.

    # Regn ut Legendre polynomet med graden n
    lPoly= legendrePolynom(n)

    # Regn ut nullpunktene til Legendre polynomet.  Dette blir x verdiene vi skal sjekke
    nullpunkter = P.polyroots(lPoly)

    # Regn ut den deriverte til Legendre polynomet.  Brukes til å regne ut vektene til hver x verdi
    polyDer = P.polyder(lPoly)

    vekter = []

    # Lag en liste med de tilsvarende vektene til punktene vi fant
    for i in nullpunkter:
        vekter.append(vekt(polyDer, i))

    # regn ut summen vi nå har
    SUM = 0

    # Regn ut summan av f(x) til alle punktene, multiplisert med den tilsvarende vekten til punktet
    for i in range(len(nullpunkter)):
        SUM += vekter[i] * nyF(nullpunkter[i])

    # Returner summen vi fant
    return SUM
