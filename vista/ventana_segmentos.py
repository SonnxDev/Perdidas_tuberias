import tkinter as tk
from tkinter import ttk, messagebox

class VentanaSegmentos(tk.Toplevel):
    def __init__(self, controlador, editar=False, segmentos_existentes=None):
        super().__init__()
        self.title("Editar Segmentos" if editar else "Ingresar Segmentos")
        self.geometry("500x500")
        self.controlador = controlador
        self.editar = editar
        self.segmentos_existentes = segmentos_existentes or []
        self.entries = []
        self.segment_count = tk.IntVar()

        self.crear_widgets()

        if self.editar:
            self.precargar_segmentos()

    def crear_widgets(self):
        tk.Label(self, text="Número de segmentos:").pack(pady=10)
        self.combo = ttk.Combobox(self, textvariable=self.segment_count, values=list(range(1, 11)), state="readonly")
        self.combo.pack()

        self.combo.bind("<<ComboboxSelected>>", self.generar_tabla)

        self.marco_tabla = tk.Frame(self)
        self.marco_tabla.pack(pady=20)

        self.boton_aceptar = tk.Button(self, text="Aceptar", command=self.enviar_datos)
        self.boton_aceptar.pack(pady=10)

    def generar_tabla(self, event=None):
        for widget in self.marco_tabla.winfo_children():
            widget.destroy()
        self.entries.clear()

        usar_hazzen = True  # Asumimos Hazzen habilitado por defecto

        columnas = ["Diámetro (m)", "Longitud (m)"]
        if usar_hazzen:
            columnas.append("Coef. Hazzen")

        for col, texto in enumerate(columnas):
            tk.Label(self.marco_tabla, text=texto, width=15, borderwidth=1, relief="solid").grid(row=0, column=col)

        for i in range(self.segment_count.get()):
            fila = []
            for j in range(len(columnas)):
                entry = tk.Entry(self.marco_tabla, width=17)
                entry.grid(row=i+1, column=j, padx=1, pady=1)
                fila.append(entry)
            self.entries.append(fila)

        if self.editar:
            self.precargar_segmentos()

    def precargar_segmentos(self):
        self.combo.set(len(self.segmentos_existentes))
        self.generar_tabla()

        for i, seg in enumerate(self.segmentos_existentes):
            self.entries[i][0].insert(0, seg.diametro)
            self.entries[i][1].insert(0, seg.longitud)
            if len(self.entries[i]) > 2 and seg.coeficiente is not None:
                self.entries[i][2].insert(0, seg.coeficiente)

    def enviar_datos(self):
        segmentos = []
        for i, fila in enumerate(self.entries):
            try:
                diametro = float(fila[0].get())
                longitud = float(fila[1].get())
                coef = float(fila[2].get()) if len(fila) > 2 else None
                segmento = self.controlador.crear_segmento(i+1, diametro, longitud, coef)
                segmentos.append(segmento)
            except ValueError:
                messagebox.showerror("Error", f"Datos inválidos en la fila {i+1}")
                return

        self.controlador.recibir_segmentos(segmentos)
        self.destroy()
