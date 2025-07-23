import matplotlib.pyplot as plt
import math

def graficar_segmentos(segmentos, resultados, H, metodo):
    fig, ax = plt.subplots(figsize=(8.5, 4.5))  # antes era (10, 5)

    # Validación de energía física
    for r in resultados:
        if r["hf"] < 0 or r["hf"] > H:
            raise ValueError(f"Segmento {r['segmento']} tiene hf fuera del rango físico.")

    x_acum = 0
    energia_actual = H
    x_points = [0]
    y_points = [H]

    for seg, r in zip(segmentos, resultados):
        L = seg.longitud
        hf = r["hf"]
        diam = seg.diametro

        x_next = x_acum + L
        y_next = energia_actual - hf

        # Línea azul: tramo físico
        ax.plot([x_acum, x_next], [energia_actual, energia_actual], color="blue", linewidth=3)
        ax.text((x_acum + x_next)/2, energia_actual + 0.5, f"Ø {diam} m", ha="center", fontsize=8)

        # Línea amarilla: pérdida energética
        ax.plot([x_acum, x_next], [energia_actual, y_next], color="gold", linestyle="--", linewidth=2)

        # Línea verde: vector hf
        ax.plot([x_next, x_next], [energia_actual, y_next], color="green", linestyle=":", linewidth=1)
        ax.text(x_next, (energia_actual + y_next)/2, f"hf={hf}", fontsize=7, color="green", rotation=90)

        # Ángulo de pérdida
        angulo_rad = math.atan(hf / L)
        angulo_deg = math.degrees(angulo_rad)
        ax.text((x_acum + x_next)/2, y_next - 0.5, f"{round(angulo_deg,1)}°", color="orange", fontsize=8)

        x_points.append(x_next)
        y_points.append(y_next)

        x_acum = x_next
        energia_actual = y_next

    ax.plot(x_points, y_points, color="red", linewidth=1, linestyle="-.")
    ax.plot([0, x_points[-1]], [H, 0], color="black", linestyle="--", linewidth=1.5, label="Referencia diagonal")

    ax.set_title(f"Perfil energético - {metodo}")
    ax.set_xlabel("Distancia (m)")
    ax.set_ylabel("Energía (m)")
    ax.grid(True)
    ax.set_xlim(0, x_points[-1] + 5)
    ax.set_ylim(0, H + 5)

    return fig