def calcular_hf_hazzen(q_l_s, diametro, longitud, c):
    q_m3_s = q_l_s / 1000
    hf = 10.674 * (q_m3_s ** 1.852) / (c ** 1.852 * diametro ** 4.871) * longitud
    return round(hf, 4)