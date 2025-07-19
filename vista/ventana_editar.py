import tkinter as tk
from tkinter import ttk, messagebox

class VentanaEditar(tk.Toplevel):
    def __init__(self, controlador, segmentos):
        super().__init__()
        self.controlador = controlador
        self.segmentos = segmentos
        self.title("Editar segmentos")
        self.geometry("500x450")
        self.entries = []
        self._crear_widgets()
        self._precargar()

    def _crear_widgets(self):
        tk.Label(self, text=f"Segmentos existentes: {len(self.segmentos)}").pack(pady=5)
        self.marco = tk.Frame(self)
        self.marco.pack(pady=10, fill="x", expand=True)
        # encabezados
        cols = ["Diámetro (m)","Longitud (m)","Coef. Hazzen"]
        for j,c in enumerate(cols):
            tk.Label(self.marco, text=c, borderwidth=1, relief="solid").grid(row=0,column=j,padx=2)
        # filas
        for i in range(len(self.segmentos)):
            fila=[]
            for j in range(len(cols)):
                e=tk.Entry(self.marco,width=12)
                e.grid(row=i+1,column=j,padx=2,pady=2)
                fila.append(e)
            self.entries.append(fila)
        tk.Button(self,text="Guardar cambios", command=self._aceptar).pack(pady=10)

    def _precargar(self):
        for i, seg in enumerate(self.segmentos):
            self.entries[i][0].insert(0, seg.diametro)
            self.entries[i][1].insert(0, seg.longitud)
            self.entries[i][2].insert(0, seg.coeficiente)

    def _aceptar(self):
        nueva=[]
        try:
            for i,row in enumerate(self.entries):
                d=float(row[0].get())
                L=float(row[1].get())
                C=float(row[2].get())
                nueva.append(self.controlador.crear_segmento(i+1,d,L,C))
        except:
            messagebox.showerror("Error","Revise los datos de edición")
            return
        self.controlador.recibir_segmentos(nueva)
        self.destroy()
