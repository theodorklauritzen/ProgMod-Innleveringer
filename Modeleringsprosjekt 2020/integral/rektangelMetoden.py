#
# En impementering av rektangelmetoden for å integrere
#

def RektangelMetoden(f, a, b, N = 100000, regel = "venstre"):
    # f : En funksjon å integrere
    # a : Starten på det bestemte integralet
    # b : Slutten på det bestemte integralet
    # N : Antall rektangler
    # regel : Hvor man skal regne ut høyden ["venstre" | "midten" | "hoyre"]

    # Regne ut hva man må legge til i for å regne høyden på riktig sted
    i_regel = 0
    if regel.lower() == "midten":
        i_regel = 0.5
    elif regel.lower() == "hoyre":
        i_regel = 1
    elif regel.lower() != "venstre":
        # Kast en feil melding hvis regel argumentet er brukt feil
        raise Exception(f"Regel må være [\"venstre\" (Standard) | \"midten\" | \"hoyre\"], men det ble spesifisert {regel}")

    # Bredden per rektangel
    dx = (b - a) / N
    # Arealet under grafen
    A = 0

    # Loop gjennom alle rekangelene
    for i in range(N):
        # Legg sammen høyden i rektanglene
        A += f(a + (i + i_regel) * dx)

    # Multipliser med bredden per integral for å finne arealet
    A *= dx

    # returner arealet under grafen f
    return A
