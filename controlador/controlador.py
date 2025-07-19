from modelo.segmento import Segmento
from vista.ventana_segmentos import VentanaSegmentos
from vista.ventana_editar import VentanaEditar
from calculos.hazzen import calcular_hf_hazzen

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.segmentos = []

    # Ventana inicial de ingreso
    def abrir_ventana_segmentos(self):
        v = VentanaSegmentos(self)
        v.grab_set()

    # Ventana de edición
    def abrir_edicion_segmentos(self):
        v = VentanaEditar(self, self.segmentos)
        v.grab_set()

    def crear_segmento(self, numero, diametro, longitud, coeficiente):
        return Segmento(numero, diametro, longitud, coeficiente)

    # Recibe lista nueva de segmentos (ingreso o edición)
    def recibir_segmentos(self, lista_segmentos):
        self.segmentos = lista_segmentos
        # Dibuja en canvas
        self.vista.dibujar_segmentos(self.segmentos)
        # Habilita edición y panel de sistema
        self.vista.habilitar_post_segmentos()

    # (más adelante) calcula según selección de métodos
    def realizar_calculo(self, usar_hazzen, usar_darcy, q_l_s, rugosidad_mm, viscosidad_cin, altura_m):
        self.metodo_hazzen_activado = usar_hazzen
        self.metodo_darcy_activado = usar_darcy
        self.q = q_l_s
        self.k = rugosidad_mm
        self.nu = viscosidad_cin * 1e-6  # convertir a m²/s
        self.h = altura_m

        # Por ahora: solo Hazzen, lo demás vendrá después
        if usar_hazzen:
            resultados = []
            total_hf = 0

            for seg in self.segmentos:
                if None in (seg.diametro, seg.longitud, seg.coeficiente):
                    continue
                from calculos.hazzen import calcular_hf_hazzen
                hf = calcular_hf_hazzen(q_l_s, seg.diametro, seg.longitud, seg.coeficiente)
                total_hf += hf
                resultados.append({
                    "segmento": seg.numero,
                    "caudal": q_l_s,
                    "coef": seg.coeficiente,
                    "diam": seg.diametro,
                    "long": seg.longitud,
                    "hf": hf
                })

            self.vista.mostrar_tabla_hazzen(resultados, total_hf)
