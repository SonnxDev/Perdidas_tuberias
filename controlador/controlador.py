from modelo.segmento import Segmento
from vista.ventana_segmentos import VentanaSegmentos
from calculos.hazzen import calcular_hf_hazzen

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.segmentos = []
        self.metodo_hazzen_activado = False

    def abrir_ventana_segmentos(self):
        ventana_seg = VentanaSegmentos(self)
        ventana_seg.grab_set()

    def abrir_edicion_segmentos(self):
        ventana_edicion = VentanaSegmentos(self, editar=True, segmentos_existentes=self.segmentos)
        ventana_edicion.grab_set()

    def crear_segmento(self, numero, diametro, longitud, coeficiente=None):
        return Segmento(numero, diametro, longitud, coeficiente)

    def recibir_segmentos(self, lista_segmentos):
        self.segmentos = lista_segmentos
        self.vista.dibujar_segmentos(self.segmentos)
        self.vista.habilitar_datos_sistema()

    def realizar_calculo(self):
        if not self.metodo_hazzen_activado or not self.segmentos:
            return

        try:
            q_l_s = float(self.vista.inputs_generales["caudal"].get())
        except:
            return

        resultados = []
        total_hf = 0

        for seg in self.segmentos:
            if None in (seg.diametro, seg.longitud, seg.coeficiente):
                continue
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
