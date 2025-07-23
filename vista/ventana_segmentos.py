import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado
import sys, os

def ruta_recurso(relativa):
    base = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    return os.path.join(base, relativa)

class VentanaSegmentos(tk.Toplevel):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.title("Ingresar segmentos")
        self.geometry("800x650")  # Ventana más ancha para acomodar la imagen a la derecha
        self.entries = []
        self._crear_widgets()

    def _crear_widgets(self):
        tk.Label(self, text="Número de segmentos (1–10):").pack(pady=5)
        self.combo = ttk.Combobox(self, values=list(range(1, 11)), state="readonly")
        self.combo.pack()
        self.combo.bind("<<ComboboxSelected>>", self._crear_tabla)

        # Contenedor horizontal para tabla e imagen
        contenedor = tk.Frame(self)
        contenedor.pack(pady=10, fill="both", expand=True)

        # Marco de tabla a la izquierda
        self.marco = tk.Frame(contenedor)
        self.marco.pack(side="left", padx=20, fill="x", expand=True)

        # Imagen a la derecha (ruta segura)
        try:
            imagen_path = ruta_recurso("recursos/imagen_segmentos.png")
            imagen = Image.open(imagen_path).resize((350, 300))
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            label_img = tk.Label(contenedor, image=self.imagen_tk)
            label_img.pack(side="right", padx=20, pady=10)
        except Exception as e:
            print("No se pudo cargar la imagen:", e)

        # Botón aceptar
        tk.Button(self, text="Aceptar", command=self._aceptar).pack(pady=10)

    def _crear_tabla(self, _=None):
        for w in self.marco.winfo_children():
            w.destroy()
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