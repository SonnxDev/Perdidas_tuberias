# vista/ventana_principal.py
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pérdida de energía en tuberías")
        self.geometry("1450x950")
        self.controlador = None
        self.segmentos_cargados = False

        # Botones de ingreso/edición
        tk.Button(self, text="Ingresar segmentos", width=30, command=self.abrir_segmentos).place(x=1100, y=20)
        self.bt_editar = tk.Button(self, text="Editar segmentos", width=30, command=self.editar_segmentos)
        self.bt_editar.place(x=1100, y=60)
        self.bt_editar.config(state="disabled")

        # Canvas para dibujar segmentos
        self.canvas = tk.Canvas(self, width=1000, height=450, bg="white")
        self.canvas.place(x=20, y=20)

        # Panel de datos del sistema
        self._crear_panel_sistema()

        # Panel de selección de métodos y botón calcular
        self._crear_panel_metodos()

    def abrir_segmentos(self):
        if self.controlador:
            self.controlador.abrir_ventana_segmentos()

    def editar_segmentos(self):
        if self.controlador:
            self.controlador.abrir_edicion_segmentos()

    def habilitar_post_segmentos(self):
        # Se llama desde el controlador tras ingresar/editar segmentos
        self.segmentos_cargados = True
        self.bt_editar.config(state="normal")
        # Habilitar entradas del sistema
        for e in self.inputs_sis.values():
            e.config(state="normal")

    def dibujar_segmentos(self, segmentos):
        # Borra dibujo previo
        self.canvas.delete("all")
        if not segmentos:
            return

        ancho = int(self.canvas["width"])
        alto = int(self.canvas["height"])
        total_L = sum(seg.longitud for seg in segmentos)
        x0, y0 = 20, 20

        for seg in segmentos:
            propor = seg.longitud / total_L
            dx = propor * (ancho - 40)
            dy = propor * (alto - 40)
            x1, y1 = x0 + dx, y0 + dy

            # Dibuja línea y nodos
            self.canvas.create_line(x0, y0, x1, y1, width=3, fill="blue")
            self.canvas.create_oval(x0-3, y0-3, x0+3, y0+3, fill="black")
            self.canvas.create_text((x0+x1)/2, (y0+y1)/2 - 10, text=f"Segmento {seg.numero}", font=("Arial", 9))

            x0, y0 = x1, y1

        # Punto final
        self.canvas.create_oval(x1-3, y1-3, x1+3, y1+3, fill="red")

    def _crear_panel_sistema(self):
        panel = tk.LabelFrame(self, text="Datos del sistema", padx=10, pady=10)
        panel.place(x=1100, y=120)
        self.inputs_sis = {}
        campos = [
            ("Caudal (L/s):", "caudal"),
            ("Rugosidad (mm):", "rugosidad"),
            ("Viscosidad cinética (x10⁻⁶ m²/s):", "viscosidad"),
            ("Altura (m):", "altura")
        ]
        for i, (texto, clave) in enumerate(campos):
            tk.Label(panel, text=texto).grid(row=i, column=0, sticky="w", pady=5)
            e = tk.Entry(panel, width=20)
            e.insert(0, "0")
            e.config(state="disabled")
            e.grid(row=i, column=1, pady=5)
            self.inputs_sis[clave] = e

    def _crear_panel_metodos(self):
        panel = tk.LabelFrame(self, text="Métodos", padx=10, pady=10)
        panel.place(x=1100, y=320)
        self.var_hazzen = tk.BooleanVar()
        self.var_darcy = tk.BooleanVar()
        tk.Checkbutton(panel, text="Hazen-Williams", variable=self.var_hazzen).pack(anchor="w")
        tk.Checkbutton(panel, text="Darcy-Weisbach", variable=self.var_darcy).pack(anchor="w")
        tk.Button(panel, text="Calcular", command=self._calcular).pack(pady=10)

    def _calcular(self):
        if not self.segmentos_cargados:
            messagebox.showwarning("Advertencia", "Primero ingrese los segmentos")
            return

        # Leer selección de métodos
        usar_h = self.var_hazzen.get()
        usar_d = self.var_darcy.get()

        # Leer datos del sistema
        try:
            q = float(self.inputs_sis["caudal"].get())
            k = float(self.inputs_sis["rugosidad"].get())
            nu = float(self.inputs_sis["viscosidad"].get())
            H = float(self.inputs_sis["altura"].get())
        except ValueError:
            messagebox.showerror("Error", "Datos del sistema inválidos")
            return

        # Llamada al controlador
        self.controlador.realizar_calculo(usar_h, usar_d, q, k, nu, H)

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