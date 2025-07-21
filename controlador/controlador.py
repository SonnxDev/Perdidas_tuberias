from modelo.segmento import Segmento
from vista.ventana_segmentos import VentanaSegmentos
from vista.ventana_editar import VentanaEditar
from calculos.hazzen import calcular_hf_hazzen
from calculos.darcy import calcular_segmento_darcy

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
        ##self.vista.dibujar_segmentos(self.segmentos)
        # Habilita edición y panel de sistema
        self.vista.habilitar_post_segmentos()

    def realizar_calculo(self, usar_hazzen, usar_darcy, q, k, nu, h):
        if not self.segmentos:
            return

        if usar_hazzen:
            resultados_hazzen = []
            total_hf_hazzen = 0
            for seg in self.segmentos:
                hf = calcular_hf_hazzen(q, seg.diametro, seg.longitud, seg.coeficiente)
                total_hf_hazzen += hf
                resultados_hazzen.append({
                    "segmento": seg.numero,
                    "caudal": q,
                    "coef": seg.coeficiente,
                    "diam": seg.diametro,
                    "long": seg.longitud,
                    "hf": hf
                })
            self.vista.mostrar_tabla_hazzen(resultados_hazzen, total_hf_hazzen)

        if usar_darcy:
            resultados_darcy = []
            total_hf_darcy = 0
            for seg in self.segmentos:
                resultado = calcular_segmento_darcy(q, seg, k, nu)
                resultado["segmento"] = seg.numero
                resultados_darcy.append(resultado)
                total_hf_darcy += resultado["hf"]
            self.vista.mostrar_tabla_darcy(resultados_darcy, total_hf_darcy)

    def calcular_hazzen(self, q):
        resultados_hazzen = []
        for seg in self.segmentos:
            hf = calcular_hf_hazzen(q, seg.diametro, seg.longitud, seg.coeficiente)
            resultados_hazzen.append({
                "segmento": seg.numero,
                "caudal": q,
                "coef": seg.coeficiente,
                "diam": seg.diametro,
                "long": seg.longitud,
                "hf": hf
            })
        return resultados_hazzen

    def calcular_darcy(self, q, k, nu):
        resultados_darcy = []
        for seg in self.segmentos:
            resultado = calcular_segmento_darcy(q, seg, k, nu)
            resultado["segmento"] = seg.numero
            resultados_darcy.append(resultado)
        return resultados_darcy
