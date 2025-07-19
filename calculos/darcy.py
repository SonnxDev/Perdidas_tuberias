import math

def calcular_reynolds(q_l_s, diametro, viscosidad_cinematica):
    area = math.pi * (diametro ** 2) / 4
    velocidad = (q_l_s / 1000) / area  # m/s
    reynolds = (velocidad * diametro) / (viscosidad_cinematica * 1e-6)
    return reynolds, velocidad


def velocidad_corte(diametro, hf, longitud):
    if hf == 0 or longitud == 0:
        return 0
    return math.sqrt((9.81 * (diametro / 4) * hf) / longitud)


def f_lisa(re, f_ini=0.02, tol=1e-6):
    f = f_ini
    while True:
        f_new = 1 / (2 * math.log10((re * math.sqrt(f)) / 2.51)) ** 2
        if abs(f_new - f) < tol:
            break
        f = f_new
    return f


def f_rugosa(d, k, f_ini=0.02, tol=1e-6):
    f = f_ini
    while True:
        f_new = 1 / (2 * math.log10((3.17 * d) / k)) ** 2
        if abs(f_new - f) < tol:
            break
        f = f_new
    return f


def f_transicional(d, k, re, f_ini=0.02, tol=1e-6):
    f = f_ini
    while True:
        arg = (k / d) / 3.71 + 2.51 / (re * math.sqrt(f))
        f_new = 1 / (-2 * math.log10(arg)) ** 2
        if abs(f_new - f) < tol:
            break
        f = f_new
    return f


def calcular_hf_darcy(f, longitud, diametro, velocidad):
    return (f * (longitud / diametro)) * ((velocidad ** 2) / (2 * 9.81))


def calcular_segmento_darcy(q_l_s, segmento, k_mm, nu):
    k = k_mm / 1000  # mm a metros
    diam = segmento.diametro
    long = segmento.longitud

    re, v = calcular_reynolds(q_l_s, diam, nu)
    tipo_flujo = "Laminar" if re <= 2000 else "Turbulento"
    tipo_tuberia = "Flujo laminar"

    if re <= 2000:
        f = 64 / re
        hf = calcular_hf_darcy(f, long, diam, v)
        vc = velocidad_corte(diam, hf, long)
    else:
        # Lisa
        f = f_lisa(re)
        hf = calcular_hf_darcy(f, long, diam, v)
        vc = velocidad_corte(diam, hf, long)
        condicion = (vc * k) / (nu * 1e-6)
        if condicion <= 5:
            tipo_tuberia = "Tubería lisa"
        elif condicion >= 70:
            tipo_tuberia = "Tubería rugosa"
            f = f_rugosa(diam, k)
            hf = calcular_hf_darcy(f, long, diam, v)
            vc = velocidad_corte(diam, hf, long)
        else:
            tipo_tuberia = "Tubería transicional"
            f = f_transicional(diam, k, re)
            hf = calcular_hf_darcy(f, long, diam, v)
            vc = velocidad_corte(diam, hf, long)

    return {
        "reynolds": round(re, 2),
        "f": round(f, 5),
        "vc": round(vc, 3),
        "tipo_flujo": tipo_flujo,
        "tipo_tubo": tipo_tuberia,
        "hf": round(hf, 4)
    }