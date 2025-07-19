import tkinter as tk
from tkinter import ttk, messagebox

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pérdida de energía en tuberías")
        self.geometry("1400x950")
        self.controlador = None
        self.segmentos_cargados = False

        self.boton_segmentos = tk.Button(self, text="Ingresar cantidad de segmentos", width=30, command=self.abrir_segmentos)
        self.boton_segmentos.place(x=1100, y=20)

        self.boton_segmentos.place(x=1100, y=20)

        self.boton_editar_segmentos = tk.Button(self, text="Editar segmentos", width=30, command=self.editar_segmentos)
        self.boton_editar_segmentos.place(x=1100, y=60)
        self.boton_editar_segmentos.config(state="disabled")

        self.canvas = tk.Canvas(self, width=1000, height=450, bg="white")
        self.canvas.place(x=20, y=20)

        self.crear_panel_datos_generales()

    def abrir_segmentos(self):
        if self.controlador:
            self.controlador.abrir_ventana_segmentos()

    def crear_panel_datos_generales(self):
        panel = tk.Frame(self)
        panel.place(x=1100, y=80)

        self.inputs_generales = {}

        campos = [
            ("Altura del sistema (m):", "altura"),
            ("Caudal del sistema (L/s):", "caudal"),
            ("Altura de rugosidad (mm):", "rugosidad"),
            ("Viscosidad cinética (x10⁻⁶ m²/s):", "viscosidad")
        ]

        for i, (texto, clave) in enumerate(campos):
            tk.Label(panel, text=texto).grid(row=i, column=0, sticky="w", pady=5)
            entrada = tk.Entry(panel, width=25)
            entrada.insert(0, "0")
            entrada.config(state="disabled")
            entrada.grid(row=i, column=1, pady=5)
            self.inputs_generales[clave] = entrada

        self.boton_calcular = tk.Button(panel, text="Calcular", width=25, command=self.ejecutar_calculo_si_hay_controlador)
        self.boton_calcular.grid(row=len(campos), column=0, columnspan=2, pady=15)
        self.boton_calcular.config(state="normal")

    def habilitar_datos_sistema(self):
        for entry in self.inputs_generales.values():
            entry.config(state="normal")
        self.segmentos_cargados = True
        self.boton_editar_segmentos.config(state="normal")  # Esto lo habilita correctamente

    def ejecutar_calculo_si_hay_controlador(self):
        if not self.segmentos_cargados:
            messagebox.showwarning("Advertencia", "Primero ingrese el número de segmentos")
            return
        if self.controlador:
            self.controlador.realizar_calculo()

    def dibujar_segmentos(self, segmentos):
        self.canvas.delete("all")
        if not segmentos:
            return

        ancho_canvas = int(self.canvas["width"])
        alto_canvas = int(self.canvas["height"])
        total_longitud = sum(seg.longitud for seg in segmentos)
        x0, y0 = 20, 20

        for seg in segmentos:
            proporcion = seg.longitud / total_longitud
            dx = proporcion * (ancho_canvas - 40)
            dy = proporcion * (alto_canvas - 40)
            x1, y1 = x0 + dx, y0 + dy
            self.canvas.create_line(x0, y0, x1, y1, width=3, fill="blue")
            self.canvas.create_oval(x0-3, y0-3, x0+3, y0+3, fill="black")
            self.canvas.create_text((x0+x1)/2, (y0+y1)/2 - 10, text=f"Segmento {seg.numero}")
            x0, y0 = x1, y1

        self.canvas.create_oval(x1-3, y1-3, x1+3, y1+3, fill='red')

    def mostrar_tabla_hazzen(self, resultados, total_hf):
        if hasattr(self, 'tabla_hazzen'):
            self.tabla_hazzen.destroy()

        marco = tk.LabelFrame(self, text="Hazen-Williams", padx=10, pady=10)
        marco.place(x=20, y=520, width=1340, height=200)

        columnas = ["Segmento", "Caudal (L/s)", "Coeficiente", "Diámetro (m)", "Longitud (m)", "hf"]
        self.tabla_hazzen = ttk.Treeview(marco, columns=columnas, show="headings", height=6)
        for col in columnas:
            self.tabla_hazzen.heading(col, text=col)
            self.tabla_hazzen.column(col, anchor="center", width=200)

        for r in resultados:
            self.tabla_hazzen.insert("", "end", values=[
                r["segmento"], r["caudal"], r["coef"], r["diam"], r["long"], r["hf"]
            ])

        self.tabla_hazzen.insert("", "end", values=["TOTAL", "", "", "", "", round(total_hf, 4)])
        self.tabla_hazzen.pack(expand=True, fill="both")

    def editar_segmentos(self):
        if self.controlador:
            self.controlador.abrir_edicion_segmentos()