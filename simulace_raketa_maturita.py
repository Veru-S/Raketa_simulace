import math   # jen kvůli odmocnině a mocninám

print ("Začátek simulace: ______________________________________________________________________")
print(" ")
# ---------- FYZIKÁLNÍ KONSTANTY ----------
g = 9.81              # gravitační zrychlení (m/s^2)
rho_w = 1000          # hustota vody (kg/m^3)
rho_air = 1.2         # hustota vzduchu (kg/m^3)
p_atm = 101325        # atmosférický tlak (Pa)
kappa = 1.4           # Poissonova konstanta pro vzduch

# ---------- PARAMETRY RAKETY ----------
m0 = 0.45              # počáteční hmotnost rakety (kg)
Vw0 = 0.0002          # objem vody (m^3) = 500 ml
Vb = 0.002            # celkový objem lahve (m^3) = 2l
p0 = 3.08e5           # počáteční tlak (Pa)
A = 1e-4              # průřez trysky (m^2)

# ---------- POČÁTEČNÍ PODMÍNKY ----------
dt = 0.001            # časový krok (s)
t = 0                 # čas
v = 0                 # rychlost
h = 0                 # výška
m = m0                # aktuální hmotnost
Vw = Vw0              # aktuální objem vody
V_air0 = Vb - Vw0     # počáteční objem vzduchu

time_water_end = None

# ---------- HLAVNÍ SIMULAČNÍ SMYČKA ----------
while True:

    # objem vzduchu v lahvi = celý objem lahve - objem vody
    V_air = Vb - Vw

    # aktuální tlak podle adiabatického děje, jak se zvětšuje objem vzduchu, tlak klesá, konstanta pV(na k)
    p = p0 * (V_air / V_air0) ** kappa

    # dokud je v raketě voda -> existuje tah; jakmile dojde voda, zbylý přebytek vzduchu už dodá pouze minimální sílu
    if Vw > 0:
        ve = math.sqrt(2 * (p - p_atm) / rho_w)                  # Bernoulliho rovnice → přeměna tlakové energie na kinetickou.
        mdot = rho_w * A * ve                                    # Kolik vody za sekundu opustí raketu, určuje klesání hmotnosti, tlaku a trvání tahu
        F = mdot * ve                                            # Základní rovnice tahu: F=m(.)*v(e)
    else:
        F = 0                                                    #není-li voda, není tah
        mdot = 0                                                 # nevytéká-li voda, není m(dot)
        if time_water_end is None:
            time_water_end = t

    # gravitační síla
    Fg = m * g                                                   

    # odpor vzduchu
  #  Fd = 0.5 * rho_air * Cd * S * v * v

    # výsledná síla
    Fnet = F - Fg                         # Newton ->

    # zrychlení rakety                                           # a=F/m
    a = Fnet / m

    # aktualizace rychlosti a výšky
    v = v + a * dt                                               # a=dv/dt -> v(t+dt)=v(t)+adt
    h = h + v * dt                                               # k výšce přičteme výšku získanou za dt, což je v*dt

    # úbytek hmotnosti
    m = m - mdot * dt                                            # hmotnost doteď - hmotnostní úbytek za dt
    Vw = Vw - (mdot / rho_w) * dt                                # objem vody - vyteklý objem vody za dt

    t = t + dt                                                   # přičte čas dt k t, pokud pojede znovu pak počítá nové podmínky atd.

   # print ("čas: ", t," s; rychlost: ", v, " m/s; zrychlení: ", a," m/s2; hmotnost: ", m," kg; objem vody: ", Vw, " ml; výška: ", h," m")
    if int(t*1000) % 50 == 0:
        print(
            "t =", round(t, 2),
            "p =", round(p/1000, 1), "kPa",
            "m =", round(m, 3), "kg",
            "Vw =", round(Vw*1000, 1), "ml",
            "v =", round(v, 2), "m/s",
            "a =", round(a, 2), "m/s^2",
            "h =", round(h, 2), "m"
        )

    # konec simulace – dosažen vrchol
    if v <= 0 and t > 0.5:                                       # pokud je v menší nebo rovna nule, raketa dosáhla vrcholu a simulace končí
        break

# ---------- VÝSTUP ----------
print("Maximální výška:", round(h, 2), "m")
print("Čas do vyčerpání vody:", round(time_water_end, 3), "s")
print("Celkový čas letu:", round(t, 2), "s")

print(" ")
print ("Konec simulace: ______________________________________________________________________")
print(" ")