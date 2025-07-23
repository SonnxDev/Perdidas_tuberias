import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graficador import graficar_segmentos
from PIL import Image, ImageTk
import sys, os

def ruta_recurso(relativa):
    base = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    return os.path.join(base, relativa)

class VentanaPrincipal(tk.Tk):
    def __init__(self, controlador):
        super().__init__()
        self.title("Pérdida de energía en tuberías")
        self.geometry("1366x768")
        self.resizable(False, False)

        self.controlador = controlador
        self.segmentos_cargados = False
        self.canvas_grafica_hazzen = None
        self.canvas_grafica_darcy = None
        self._colocar_logo()

        # Frame desplazable para resultados
        self.frame_resultados = tk.Frame(self)
        self.frame_resultados.place(x=20, y=20, width=950, height=720)

        self.canvas_scroll = tk.Canvas(self.frame_resultados)
        self.scrollbar = tk.Scrollbar(self.frame_resultados, orient="vertical", command=self.canvas_scroll.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas_scroll)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(scrollregion=self.canvas_scroll.bbox("all"))
        )
        self.canvas_scroll.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_scroll.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_scroll.pack(side="left", fill="both", expand=True)

        self._crear_panel_sistema()
        self._crear_panel_metodos()
        self._crear_botones()

    def _crear_botones(self):
        x = 1000  # Más cerca del borde derecho
        tk.Button(self, text="Ingresar segmentos", width=28, command=self.abrir_segmentos).place(x=x, y=20)
        self.bt_editar = tk.Button(self, text="Editar segmentos", width=28, command=self.editar_segmentos)
        self.bt_editar.place(x=x, y=60)
        self.bt_editar.config(state="disabled")

        if self.controlador:
            tk.Button(self, text="Calcular distancias por hf", width=28,
                      command=self.controlador.abrir_ventana_calcular_distancias).place(x=x, y=100)

    def _colocar_logo(self):
        try:
            logo_path = ruta_recurso("recursos/logo_programa.png")
            logo = Image.open(logo_path).convert("RGBA").resize((100, 100))
            logo_tk = ImageTk.PhotoImage(logo)
            self.label_logo = tk.Label(self, image=logo_tk, bg="white")
            self.label_logo.image = logo_tk
            self.label_logo.place(x=1040, y=580)

            self.label_firma = tk.Label(self, text="Camargo Meza, Bryan Miguel", font=("Arial", 9, "italic"),
                                        bg="white", fg="gray30")
            self.label_firma.place(x=1040, y=690)
        except Exception as e:
            print("No se pudo cargar el logo:", e)

    def abrir_segmentos(self):
        if self.controlador:
            self.controlador.abrir_ventana_segmentos()

    def editar_segmentos(self):
        if self.controlador:
            self.controlador.abrir_edicion_segmentos()

    def habilitar_post_segmentos(self):
        self.segmentos_cargados = True
        self.bt_editar.config(state="normal")
        for e in self.inputs_sis.values():
            e.config(state="normal")

    def _crear_panel_sistema(self):
        panel = tk.LabelFrame(self, text="Datos del sistema", padx=10, pady=10)
        panel.place(x=1000, y=140)
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
        panel.place(x=1000, y=300)
        self.var_hazzen = tk.BooleanVar()
        self.var_darcy = tk.BooleanVar()
        self.var_ver_hazzen = tk.BooleanVar()
        self.var_ver_darcy = tk.BooleanVar()

        tk.Checkbutton(panel, text="Usar Hazen-Williams", variable=self.var_hazzen).pack(anchor="w")
        tk.Checkbutton(panel, text="Usar Darcy-Weisbach", variable=self.var_darcy).pack(anchor="w")
        tk.Checkbutton(panel, text="Ver gráfica Hazen", variable=self.var_ver_hazzen).pack(anchor="w")
        tk.Checkbutton(panel, text="Ver gráfica Darcy", variable=self.var_ver_darcy).pack(anchor="w")
        tk.Button(panel, text="Calcular", command=self._calcular).pack(pady=10)

    def _calcular(self):
        if not self.segmentos_cargados:
            messagebox.showwarning("Advertencia", "Primero ingrese los segmentos")
            return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        usar_h = self.var_hazzen.get()
        usar_d = self.var_darcy.get()
        ver_h = self.var_ver_hazzen.get()
        ver_d = self.var_ver_darcy.get()

        try:
            q = float(self.inputs_sis["caudal"].get())
            k = float(self.inputs_sis["rugosidad"].get())
            nu = float(self.inputs_sis["viscosidad"].get())
            H = float(self.inputs_sis["altura"].get())
        except ValueError:
            messagebox.showerror("Error", "Datos del sistema inválidos")
            return

        resultados_hazzen = []
        resultados_darcy = []

        if usar_h:
            resultados_hazzen = self.controlador.calcular_hazzen(q)
            if resultados_hazzen:
                total_hf_hazzen = sum(r["hf"] for r in resultados_hazzen)
                self.mostrar_tabla_hazzen(resultados_hazzen, total_hf_hazzen)

        if usar_d:
            resultados_darcy = self.controlador.calcular_darcy(q, k, nu)
            if resultados_darcy:
                total_hf_darcy = sum(r["hf"] for r in resultados_darcy)
                self.mostrar_tabla_darcy(resultados_darcy, total_hf_darcy)

        if ver_h:
            for r in resultados_hazzen:
                if r["hf"] < 0 or r["hf"] > H:
                    messagebox.showerror("Sistema no admisible", f"Hazen-Williams: segmento {r['segmento']} tiene hf fuera de rango.")
                    return

        if ver_d:
            for r in resultados_darcy:
                if r["hf"] < 0 or r["hf"] > H:
                    messagebox.showerror("Sistema no admisible", f"Darcy-Weisbach: segmento {r['segmento']} tiene hf fuera de rango.")
                    return

        # Limpiar gráficos previos
        if self.canvas_grafica_hazzen:
            self.canvas_grafica_hazzen.get_tk_widget().destroy()
            self.canvas_grafica_hazzen = None
        if self.canvas_grafica_darcy:
            self.canvas_grafica_darcy.get_tk_widget().destroy()
            self.canvas_grafica_darcy = None

        try:
            if ver_h:
                fig_h = graficar_segmentos(self.controlador.segmentos, resultados_hazzen, H, "Hazen-Williams")
                self.canvas_grafica_hazzen = FigureCanvasTkAgg(fig_h, master=self.scrollable_frame)
                self.canvas_grafica_hazzen.draw()
                self.canvas_grafica_hazzen.get_tk_widget().pack(pady=10)

            if ver_d:
                fig_d = graficar_segmentos(self.controlador.segmentos, resultados_darcy, H, "Darcy-Weisbach")
                self.canvas_grafica_darcy = FigureCanvasTkAgg(fig_d, master=self.scrollable_frame)
                self.canvas_grafica_darcy.draw()
                self.canvas_grafica_darcy.get_tk_widget().pack(pady=10)

        except ValueError as err:
            messagebox.showerror("Error físico", str(err))
            return

    def mostrar_tabla_hazzen(self, resultados, total_hf):
        if hasattr(self, 'tabla_hazzen'):
            self.tabla_hazzen.destroy()

        marco = tk.LabelFrame(self.scrollable_frame, text="Hazen-Williams", padx=10, pady=10)
        marco.pack(pady=10, fill="x")

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

    def mostrar_tabla_darcy(self, resultados, total_hf):
        if hasattr(self, 'tabla_darcy'):
            self.tabla_darcy.destroy()

        marco = tk.LabelFrame(self.scrollable_frame, text="Darcy-Weisbach", padx=10, pady=10)
        marco.pack(pady=10, fill="x")

        columnas = ["Segmento", "Número de Reynolds", "f", "Vc", "Tipo de flujo", "Tipo de tubería", "hf"]
        self.tabla_darcy = ttk.Treeview(marco, columns=columnas, show="headings", height=6)
        for col in columnas:
            self.tabla_darcy.heading(col, text=col)
            self.tabla_darcy.column(col, anchor="center", width=180)

        for r in resultados:
            self.tabla_darcy.insert("", "end", values=[
                r["segmento"], r["reynolds"], r["f"], r["vc"], r["tipo_flujo"], r["tipo_tubo"], r["hf"]
            ])

        self.tabla_darcy.insert("", "end", values=["TOTAL", "", "", "", "", "", round(total_hf, 4)])
        self.tabla_darcy.pack(expand=True, fill="both")