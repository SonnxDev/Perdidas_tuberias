def calcular_reynolds(v, D, nu):
    """
    Calcula el número de Reynolds y clasifica el tipo de flujo.

    Parámetros:
    - v: velocidad del fluido (m/s)
    - D: diámetro interno de la tubería (m)
    - nu: viscosidad cinemática (m²/s)

    Retorna:
    - Re: número de Reynolds
    - tipo: string con tipo de flujo
    """
    Re = (v * D) / nu
    if Re < 2000:
        tipo = "Flujo laminar"
    elif 2000 <= Re <= 4000:
        tipo = "Flujo transicional"
    else:
        tipo = "Flujo turbulento"
    return Re, tipo