import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VentanaCalcularDistancias(tk.Toplevel):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Calcular distancias de segmentos")
        self.geometry("900x600")
        self._crear_widgets()

    def _crear_widgets(self):
        # Panel de entrada de datos
        frame_inputs = tk.Frame(self)
        frame_inputs.pack(padx=10, pady=10, fill="x")

        labels = [
            "Caudal Q (m³/s)",
            "Longitud total L (m)",
            "Diámetro seg. 1 D1 (m)",
            "Diámetro seg. 2 D2 (m)",
            "Coef. Hazen C1",
            "Coef. Hazen C2",
            "hf admisible (m)"
        ]
        self.vars = {}
        for i, texto in enumerate(labels):
            tk.Label(frame_inputs, text=texto).grid(row=i, column=0, sticky="w", pady=2)
            var = tk.DoubleVar(value=0.0)
            tk.Entry(frame_inputs, textvariable=var, width=20).grid(row=i, column=1, pady=2, padx=5)
            self.vars[texto] = var

        tk.Button(
            frame_inputs,
            text="Calcular distancias",
            command=self._calcular
        ).grid(row=len(labels), column=0, columnspan=2, pady=10)

        # Contenedor para gráfica y tabla de resultados
        contenedor = tk.Frame(self)
        contenedor.pack(fill="both", expand=True)

        # Área de gráfica (izquierda)
        frame_plot = tk.Frame(contenedor)
        frame_plot.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Tabla de resultados (derecha)
        frame_tabla = tk.Frame(contenedor)
        frame_tabla.pack(side="right", padx=10, pady=10)

        cols = ("Segmento", "sf (m/m)", "hf (m)", "Longitud (m)")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=2)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center", width=100)
        self.tree.pack()

    def _calcular(self):
        try:
            Q = self.vars["Caudal Q (m³/s)"].get()
            L_total = self.vars["Longitud total L (m)"].get()
            D1 = self.vars["Diámetro seg. 1 D1 (m)"].get()
            D2 = self.vars["Diámetro seg. 2 D2 (m)"].get()
            C1 = self.vars["Coef. Hazen C1"].get()
            C2 = self.vars["Coef. Hazen C2"].get()
            hf_adm = self.vars["hf admisible (m)"].get()

            # Fórmula Hazen-Williams: sf = 10.67 * Q^1.852 / (C^1.852 * D^4.87)
            sf1 = 10.67 * Q**1.852 / (C1**1.852 * D1**4.87)
            sf2 = 10.67 * Q**1.852 / (C2**1.852 * D2**4.87)

            # Despeje de la longitud X del segundo segmento:
            # X2 = (sf1 * L_total - hf_adm) / (sf1 - sf2)
            X2 = (sf1 * L_total - hf_adm) / (sf1 - sf2)
            X1 = L_total - X2

            hf1 = sf1 * X1
            hf2 = sf2 * X2

        except Exception as e:
            messagebox.showerror("Error", f"Revisa los datos de entrada.\n{e}")
            return

        # Mostrar en la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.insert("", "end", values=(1, round(sf1, 5), round(hf1, 5), round(X1, 3)))
        self.tree.insert("", "end", values=(2, round(sf2, 5), round(hf2, 5), round(X2, 3)))

        # Dibujar gráfica aproximada
        self.ax.clear()
        # Segmento 1
        self.ax.plot([0, X1], [0, hf1], marker="o", label="Segmento 1")
        # Segmento 2
        self.ax.plot([X1, L_total], [hf1, hf1 + hf2], marker="o", label="Segmento 2")
        self.ax.set_xlabel("Longitud (m)")
        self.ax.set_ylabel("hf (m)")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()