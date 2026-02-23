import math   # jen kvůli odmocnině a mocninám

print("Začátek simulace: ______________________________________________________________________")
print(" ")

# ---------- FYZIKÁLNÍ KONSTANTY ----------
g = 9.81              # gravitační zrychlení (m/s^2)
rho_w = 1000          # hustota vody (kg/m^3)
rho_air = 1.2         # hustota vzduchu (kg/m^3)
p_atm = 101325        # atmosférický tlak (Pa)
kappa = 1.4           # Poissonova konstanta pro vzduch

# ---------- PARAMETRY RAKETY ----------
m0 = 0.244             # počáteční hmotnost rakety (kg)
Vw0 = 0.0002           # objem vody (m^3)
Vb = 0.002             # celkový objem lahve (m^3)

# tlak z pumpy je přetlak -> přepočet psi na Pa
p0_psi = 30           #30, 40 nebo 50
p0_gauge = p0_psi * 6894.76
p0 = p_atm + p0_gauge   # absolutní tlak v lahvi

# průřez trysky pro průměr 9 mm
d_nozzle = 0.009
A = math.pi * (d_nozzle / 2) ** 2

# ---------- POČÁTEČNÍ PODMÍNKY ----------
dt = 0.001            # časový krok (s)
t = 0                 # čas
v = 0                 # rychlost
h = 0                 # výška
m = m0                # aktuální hmotnost

Vw = Vw0              # aktuální objem vody
V_air0 = Vb - Vw0      # počáteční objem vzduchu

time_water_end = None

# ---------- HLAVNÍ SIMULAČNÍ SMYČKA ----------
while True:

    # objem vzduchu v lahvi = celý objem lahve - objem vody
    V_air = Vb - Vw

    # tlak podle adiabatického děje (absolutní tlak)
    p = p0 * (V_air / V_air0) ** kappa

    # dokud je v raketě voda -> existuje tah
    if Vw > 0:
        ve = math.sqrt(2 * (p ) / rho_w)
        mdot = rho_w * A * ve
        F = mdot * ve
    # elif když je ještě tlak
    # ve s normálním ró
    # mdot je jiné protože vzduch je stlačený, ró vzduchu
    # menší časový krok, 2 litry vzduchu se rychlostí zvuku vyfouknou za zlomek vteřiny
    else:
        F = 0
        mdot = 0
        if time_water_end is None:
            time_water_end = t

    # gravitační síla
    Fg = m * g                                                   

    # výsledná síla
    Fnet = F - Fg

    # zrychlení
    a = Fnet / m

    # aktualizace rychlosti a výšky
    v = v + a * dt
    h = h + v * dt

    # úbytek hmotnosti a vody
    m = m - mdot * dt
    Vw = Vw - (mdot / rho_w) * dt

    t = t + dt

  #  if int(t*1000) % 50 == 0:
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
    if v <= 0 and t > 0.5:
        break

# ---------- VÝSTUP ----------
print("Maximální výška:", round(h, 2), "m")
print("Čas do vyčerpání vody:", round(time_water_end, 3), "s")
print("Celkový čas letu:", round(t, 2), "s")

print(" ")
print ("Konec simulace: ______________________________________________________________________")
print(" ")
