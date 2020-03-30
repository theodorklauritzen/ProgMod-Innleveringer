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

    # Set ret til det polynomet med størst grad
    ret = poly1
    add = poly2

    if len(ret) < len(add):
        ret = poly2
        add = poly1

    # Legg det minste polynomet til det største
    for i in range(len(add)):
        ret[i] += add[i]

    # Returner resultatet
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

    # Returner resultatet
    return ret

# Denne funksjonene tar et polynom og returnerer en funksjon som gir y-verdiene til polynomet gitt x-verdien
def fPoly(poly):
    # poly : Et polynom å returnere funksjonsuttrykket til

    # Et funksjons uttrykk til polynomet
    def f(x):
        # x : En verdi å regne ut den tilsvarende y-verdien til

        ret = 0

        # Regn ut verdien til funksjonsuttrykket i punktet x
        for i in range(len(poly)):
            ret += poly[i] * (x ** i)

        # Returner resultatet
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
        # Sett c midt i mellom a og b
        c = (a + b) / 2

        # Se om c nærmere nok 0
        if abs(f(c)) < tol:
            # Returner c hvis det er nærme nok 0
            return c

        # Hvis nullpunktet er mellom a og c, sett b til c
        if f(a) * f(c) < 0:
            b = c
        # Hvis nullpunktet er mellom c og b, sett a til c
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

    # Finn bredden til hvert søkeområde
    dx = (b - a) / N

    # En liste med nullpunkter å returnere
    ret = []

    # Finn nullpunktene
    for i in range(N):
        n = halvveringsmetoden(f, a + dx * i, a + dx * (i + 1), tol)
        # Hvis halvveringsmetoden returnerte et nullpunkt legg det til i lista
        if not n is None:
            ret.append(n)

    # Returner lista med nullpunkter
    return ret

# En funksjon som returnerer nullpunktene til et legendrepolynom
def legendreNullpunkter(n, tol = 1e-8):
    # n : Graden til legendre polynomet
    # tol : toleransen på hvor nærme 0 et nullpunkt kan være

    # Regn ut legendre polynomet
    p = legendrePolynom(n)
    # Få et uttrykk ut i fra polynomet
    f = fPoly(p)

    # IDEA: Finn antall nullpunkter, og jskke om det stemmer
    #antallNullpunkter = math.floor(n / 2)

    # Her finner vi bare mellom 0 og 1, så kan vi regne ut de negative nullpunktene etterpå
    # Da blir progemmet raskere
    nullp = nullpunkter(f, 0, 1, tol)

    # Regn ut de ekstra nullpunktene
    ekstraNullpunkter = []
    # Sjekk om 0 er med i nullpunktene vi fant, så må vi ikke legge 0 igjen
    # Hvis n er et oddetall har vi 0 i lista, så da må vi ikke legge til dette igjen
    inneholder0 = -1 if n % 2 == 0 else 0
    # Loop gjennom baklengs for å til slutt få alt i stigende rekkefølge.
    for i in range(len(nullp) - 1, inneholder0, -1):
        ekstraNullpunkter.append(-nullp[i])

    # Returner alle nullpunktene
    return ekstraNullpunkter + nullp

# En funksjon for å gi momentan vekstfart i et punkt
def derF(f, x, h = 1e-8):
    # f : en funksjon å derivere
    # x : Et punkt å finne momentan vekst vekstfart
    # h : Et lite tall for å regne ut en liten økning

    # Returner stigningen i punktet x
    return (f(x + h) - f(x - h)) / (2 * h)

# En funksjon som finner en vekt til en x verdi
def weight(P, x):
    # P : et legendre funksjonsuttrykk
    # x : x å finne vekten til

    # w_i = 2 / ((1 - x_i^2) * (P_n'(x_i))^2 )

    return 2 / ((1 - x ** 2)  * (derF(P, x) ** 2))

# En funksjon som tar punkter på en graf og vekter og regner ut summen av dem
def calcValue(f, punkter, weights):
    # f : en funksjon
    # punkter : en liste med nullpunkter
    # weights : en like lang liste med vekter til punktene

    ret = 0

    # Regn ut summan av f(x) til alle punktene, multiplisert med den tilsvarende vekten til punktet
    for i in range(len(punkter)):
        ret += weights[i] * f(punkter[i])

    # Returner resultatet
    return ret

# En funksjon som bruker Gauss kvadratur til å regne integralet mellom -1 og 1
def GaussIntegral1(f, n, brukCache = True):
    # f : en funksjon å regne ut integralet til
    # n : graden til legendrepolynomet
    # brukCache : Om vi skal bruke hardcodede verdier i stedet for å regne dem ut, gitt at vi har punktet til den tilsvarende graden

    # Sjekk om vi skal bruke chachen
    if brukCache and len(gaussPointsWeights) >= n:
        # Hent ut punktene og vektene til cachen
        points, weights = gaussPointsWeights[n - 1]
        # Returner resultatet av kaklueringen til punktene og vektene
        return calcValue(nyF, points, weights)

    # Finn x verdien til punktene vi skal regne ut
    nullp = legendreNullpunkter(n, tol = 1e-13)

    # Regn ut Legendre polynomet med graden n
    lPoly = legendrePolynom(n)
    # Lag et funksjonsuttrykk av Legendre polynomet
    lf = fPoly(lPoly)

    weights = []

    # Lag en liste med de tilsvarende vektene til punktene vi fant
    for i in nullp:
        weights.append(weight(lf, i))

    # Returner resultatet av kakuleringen til punktene og vektene
    return calcValue(f, nullp, weights)

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
def GaussKvadratur(f, a = -1, b = 1, N = 25, brukCache = True):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Hvilken grad vi skal ha av polynomet

    # NOTE: Sjekk om N er et oddetall, se https://www.youtube.com/watch?v=Hu6yqs0R7GA&t=523
    # Fordi vi må ha en partall antall ukjente
    # Da må vi ha et partall antall ledd i polynomet
    # Dette skrever at polynommet er av grad k, der k er et oddetall
    #
    # Sjekk at N er et oddetall større enn 0
    if N % 2 == 0 or N < 1:
        # Kast en feil hvis N er spesiefisert feil
        raise Exception("N må være et oddetall større enn 0")

    # Regn ut legendre graden til den tilsvarende graden av polynomet som ble spesifisert
    legendreGrad = int((N + 1) / 2)

    # Skvis funksjonen ned så a blir liggende på -1 og b på 1.
    nyF = endreIntervall(f, a, b)

    # Returner Gausintegralet til nyF mellom -1 og 1
    return GaussIntegral1(nyF, legendreGrad, brukCache)
