import tkinter as tk
from tkinter import ttk, messagebox

class VentanaSegmentos(tk.Toplevel):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Ingresar segmentos")
        self.geometry("500x450")
        self.entries = []
        self._crear_widgets()

    def _crear_widgets(self):
        tk.Label(self, text="Número de segmentos (1–10):").pack(pady=5)
        self.combo = ttk.Combobox(self, values=list(range(1,11)), state="readonly")
        self.combo.pack()
        self.combo.bind("<<ComboboxSelected>>", self._crear_tabla)

        self.marco = tk.Frame(self)
        self.marco.pack(pady=10, fill="x", expand=True)

        tk.Button(self, text="Aceptar", command=self._aceptar).pack(pady=10)

    def _crear_tabla(self, _=None):
        # limpia
        for w in self.marco.winfo_children(): w.destroy()
        self.entries.clear()

        n = int(self.combo.get())
        cols = ["Diámetro (m)", "Longitud (m)", "Coef. Hazzen"]
        for j, c in enumerate(cols):
            tk.Label(self.marco, text=c, borderwidth=1, relief="solid").grid(row=0,column=j,padx=2)
        for i in range(n):
            fila = []
            for j in range(len(cols)):
                e = tk.Entry(self.marco, width=12)
                e.grid(row=i+1,column=j,padx=2,pady=2)
                fila.append(e)
            self.entries.append(fila)

    def _aceptar(self):
        segmentos=[]
        try:
            for i, row in enumerate(self.entries):
                d = float(row[0].get())
                L = float(row[1].get())
                C = float(row[2].get())
                segmentos.append(self.controlador.crear_segmento(i+1,d,L,C))
        except:
            messagebox.showerror("Error","Revise los datos de segmentos")
            return

        self.controlador.recibir_segmentos(segmentos)
        self.destroy()
