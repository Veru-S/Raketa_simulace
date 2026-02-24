import math

print("Začátek simulace: ______________________________________________________________________")
print(" ")

# ============================================================
# FYZIKÁLNÍ KONSTANTY
# ============================================================

g = 9.81              # gravitační zrychlení (m/s^2)
rho_w = 1000          # hustota vody (kg/m^3)
rho_air_ambient = 1.2 # hustota okolního vzduchu (kg/m^3)
p_atm = 101325        # atmosférický tlak (Pa)
kappa = 1.4           # Poissonova konstanta pro vzduch
R = 287               # měrná plynová konstanta vzduchu (J/kgK)
T = 300               # uvažovaná teplota vzduchu (K)

# ============================================================
# PARAMETRY RAKETY
# ============================================================

ms = 0.244            # suchá hmotnost rakety (kg)
Vw0 = 0.0002          # počáteční objem vody (m^3) - 200ml/400ml
Vb = 0.002            # objem lahve (m^3) - 2l

m0 = ms + rho_w * Vw0 # počáteční hmotnost (raketa + voda)

# tlak z pumpy je přetlak → převod z psi na Pa
p0_psi = 40                        #30psi/40psi/50psi
p0_gauge = p0_psi * 6894.76
p0 = p_atm + p0_gauge     # absolutní tlak v lahvi

# průměr trysky 9 mm
d_nozzle = 0.009
A = math.pi * (d_nozzle/2)**2   # průřez trysky (m^2)

# ============================================================
# POČÁTEČNÍ PODMÍNKY
# ============================================================

dt = 0.0001           # menší krok kvůli vzduchové fázi
t = 0
v = 0
h = 0
m = m0

Vw = Vw0
V_air0 = Vb - Vw0

# počáteční hmotnost vzduchu v lahvi
m_air = (p0 * V_air0) / (R * T)

time_water_end = None

# ============================================================
# HLAVNÍ SMYČKA
# ============================================================

while True:

    # --------------------------------------------------------
    # OBJEM A TLAK
    # --------------------------------------------------------

    V_air = Vb - Vw

    if Vw > 0:
        # adiabatická expanze během vytlačování vody
        p = p0 * (V_air0 / V_air) ** kappa
    else:
        # po vytečení vody je objem konstantní
        # tlak určujeme z ideálního plynu
        rho_inside = m_air / Vb
        p = rho_inside * R * T

    # --------------------------------------------------------
    # FÁZE 1 – VODA
    # --------------------------------------------------------

    if Vw > 0 and p > p_atm:

        # Bernoulli pro kapalinu
        ve = math.sqrt(2 * (p - p_atm) / rho_w)

        # hmotnostní tok vody
        mdot = rho_w * A * ve

        # tah = změna hybnosti proudu
        F = mdot * ve

    # --------------------------------------------------------
    # FÁZE 2 – VZDUCH
    # --------------------------------------------------------

    elif Vw <= 0 and p > p_atm:

        # hustota vzduchu uvnitř lahve
        rho_inside = m_air / Vb

        # Bernoulli mezi lahví a výstupem
        ve = math.sqrt(2 * (p - p_atm) / rho_inside)

        # hmotnostní tok plynu
        mdot = rho_inside * A * ve

        # tah plynu (hybnostní + tlaková složka)
        F = mdot * ve + A * (p - p_atm)

        # úbytek hmotnosti vzduchu
        m_air -= mdot * dt
        m -= mdot * dt

    else:
        F = 0
        mdot = 0

        if time_water_end is None:
            time_water_end = t

    # --------------------------------------------------------
    # POHYB RAKETY
    # --------------------------------------------------------

    Fg = m * g
    Fnet = F - Fg
    a = Fnet / m

    v += a * dt
    h += v * dt

    # úbytek vody
    if Vw > 0:
        Vw -= (mdot / rho_w) * dt
        m -= mdot * dt
        if Vw < 0:
            Vw = 0

    t += dt

    print(
        "t =", round(t,3),
        "p =", round(p/1000,1),"kPa",
        "v =", round(v,2),
        "a =", round(a,2),
        "h =", round(h,2)
    )

    if v <= 0 and t > 0.5:
        break


# ============================================================
# VÝSTUP
# ============================================================

print("Maximální výška:", round(h,2),"m")
print("Čas do vyčerpání vody:", round(time_water_end,3),"s")
print("Celkový čas letu:", round(t,2),"s")

print(" ")

print("Konec simulace: ______________________________________________________________________")
