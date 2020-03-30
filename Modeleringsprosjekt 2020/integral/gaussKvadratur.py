#
# En impementering av Gauss Kvadratur for å integrere
#

import math
from .gaussKvadraturWeights import gaussPointsWeights

#
# I dette programmet er polynomer representert som en lise.
# Et eksempel på et polynom er [c, b, a]
# Siden index 0 inne holder c, blir verdien her c * x^0 = c.  Altså er c konstantelddet
# b er i index 1, så da blir verdien b * x^1 = b x
# a er i index 2, så da blir verdien a * x^2 = a x^2
#
# Polynomet vi da har er: a * x^2 + b * x + c
#

# Multipliserer to polynomer
def pMult(poly1, poly2):
    # poly1 : Et polynom vi skal multiplisere med et polynom
    # poly2 : Et polynom vi skal multiplisere med et polynom

    # Kalkuler graden til polynom produktet
    grad = len(poly1) + len(poly2) - 1
    ret = [0] * grad if grad > 0 else 1

    # Regn ut polynom produktet
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            ret[i + j] += poly1[i] * poly2[j]

    # Returner polynom produktet
    return ret

# Legger sammen to polynomer
def pAdd(poly1, poly2):
    # poly1 : Et polynom vi skal multiplisere med et polynom
    # poly2 : Et polynom vi skal multiplisere med et polynom

    ret = poly1
    add = poly2

    if len(ret) < len(add):
        ret = poly2
        add = poly1

    for i in range(len(add)):
        ret[i] += add[i]

    return ret

# Denne funksjonene returnerer Legendre polynomene
# https://en.wikipedia.org/wiki/Legendre_polynomials
def legendrePolynom(n):
    # n : graden til Legendre polynomet

    # IDEA: kanskje bruke en eksplisitt formel

    # Rekursiv formel: https://en.wikipedia.org/wiki/Legendre_polynomials#Definition_via_generating_function
    # (n + 1) P_{n + 1}(x) = (2n + 1)xP_n(x) - n P_{n - 1}(x)

    # Dette er initsialbetingelsene til den rekursive formelen
    if n == 0:
        return [1]

    if n == 1:
        return [0, 1]

    # Så bruker vi den rekursive formelen videre
    # n P_n(x) = (2n - 1)xP_{n - 1}(x) - (n - 1) P_{n - 2}(x)

    ret = pMult([0, 2 * n - 1], legendrePolynom(n - 1))
    ret = pAdd(ret, pMult(legendrePolynom(n - 2), [-(n - 1)]))

    ret = pMult(ret, [1 / n])

    return ret

# Denne funksjonene tar et polynom og returnerer en funksjon som gir y-verdiene til polynomet gitt x-verdien
def fPoly(poly):
    # poly : Et polynom å returnere funksjonsuttrykket til

    def f(x):
        # x : En verdi å regne ut den tilsvarende y-verdien til

        ret = 0

        for i in range(len(poly)):
            ret += poly[i] * (x ** i)

        return ret

    # Returner funksjonen
    return f

# En funksjon som finner et nullpunkt i et intervall
def halvveringsmetoden(f, a, b, tol = 1e-8):
    # f : En funksjon å finne nullpunktet til
    # a : Starten på intervallet vi skal lete i
    # b : Slutten på intervallet vi skal lete i
    # tol : Toleransen på hvor nærme null vi kan være

    # Sjekk om det finnes nullpunkter i intervallet
    if f(a) * f(b) > 0:
        return None
    # Sjekk om x = a er et nullpunk
    elif f(a) == 0:
        return a
    # Sjekk om x = b er et nullpunkt
    elif f(b) == 0:
        return b

    # Loop maksimum 10000 ganger
    for i in range(10000):
        c = (a + b) / 2

        if abs(f(c)) < tol:
            return c

        if f(a) * f(c) < 0:
            b = c
        elif f(c) * f(b) < 0:
            a = c

    # Hvis vi har kjørt loppen 10000 gangre stoppre vi og returnerer 0
    return None

# En funksjon som finner nullpunktene til en funksjon
def nullpunkter(f, a, b, tol = 1e-8, N = 50):
    # f : En funksjon å finne nullpunkter til
    # a : starten på intervallet å lete i
    # b : Slutten på intervaller å lete i
    # tol : toleransen på hvor nærme vi kan være nullpunktene
    # N : antall søkeområde vi deler inn i

    dx = (b - a) / N

    ret = []

    # Finn nullpunkter
    for i in range(N):
        n = halvveringsmetoden(f, a + dx * i, a + dx * (i + 1), tol)
        if not n is None:
            ret.append(n)

    return ret

# En funksjon som returnerer nullpunktene til et legendrepolynom
def legendreNullpunkter(n, tol = 1e-8):
    # n : Graden til legendre polynomet
    # tol : toleransen på hvor nærme 0 et nullpunkt kan være

    p = legendrePolynom(n)
    f = fPoly(p)

    antallNullpunkter = math.floor(n / 2)
    # Her finner vi bare mellom 0 og 1, så kan vi regne ut de negative nullpunktene etterpå
    # Da blir progemmet raskere
    nullp = nullpunkter(f, 0, 1, tol)

    ekstraNullpunkter = []
    inneholder0 = -1 if n % 2 == 0 else 0
    for i in range(len(nullp) - 1, inneholder0, -1):
        ekstraNullpunkter.append(-nullp[i])

    return ekstraNullpunkter + nullp

# En funksjon for å gi momentan vekstfart i et punkt
def derF(f, x, h = 1e-8):
    # f : en funksjon å derivere
    # x : Et punkt å finne momentan vekst vekstfart
    # h : Et lite tall for å regne ut en liten økning

    return (f(x + h) - f(x - h)) / (2 * h)

# En funksjon som finner en vekt til en x verdi
def weight(P, x):
    # P : et legendre funksjonsuttrykk
    # x : x å finne vekten til

    # w_i = 2 / ((1 - x_i^2) * (P_n'(x_i))^2 )

    return 2 / ((1 - x ** 2)  * (derF(P, x) ** 2))

# En funksjon som tar punkter på en graf og vekter og regner ut summen av dem
def calcValue(f, punkter, weights):
    ret = 0

    for i in range(len(punkter)):
        ret += weights[i] * f(punkter[i])

    return ret

# En funksjon som bruker Gauss kvadratur til å regne integralet mellom -1 og 1
def GaussIntegral1(f, n):
    # f : en funksjon å regne ut integralet til
    # n : graden til legendrepolynomet

    nullp = legendreNullpunkter(n, tol = 1e-13)

    lPoly = legendrePolynom(n)
    lf = fPoly(lPoly)

    weights = []

    for i in nullp:
        weights.append(weight(lf, i))

    return calcValue(f, nullp, weights)

# En fuksjon som returerer en annen funksjon
def endreIntervall(f, a, b):
    # f : en funksjon
    # a : starten på et intervall
    # b : slutten på et intervall

    # En funksjon å returnere
    def ret(x):
        # x : en verdi å regne ut den tilsvarende verdien til

        return (b - a) / 2 * f((b - a) / 2 * x + (a + b) / 2)

    return ret

def GaussKvadratur(f, a = -1, b = 1, N = 25, brukCache = True):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Hvilken grad vi skal ha av polynomet

    # NOTE: Sjekk om N er et oddetall, se https://www.youtube.com/watch?v=Hu6yqs0R7GA&t=523
    # Fordi vi må ha en partall antall ukjente
    # Da må vi ha et partall antall ledd i polynomet
    # Dette skrever at polynommet er av grad k, der k er et oddetall
    if N % 2 == 0 or N < 1:
        raise Exception("N må være et oddetall større enn 0")

    legendreGrad = int((N + 1) / 2)

    nyF = endreIntervall(f, a, b)

    if brukCache and len(gaussPointsWeights) >= legendreGrad:
        points, weights = gaussPointsWeights[legendreGrad - 1]
        return calcValue(nyF, points, weights)

    return GaussIntegral1(nyF, legendreGrad)
