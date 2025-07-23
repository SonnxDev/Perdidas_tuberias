import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado
import sys, os

def ruta_recurso(relativa):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relativa)

class VentanaEditar(tk.Toplevel):
    def __init__(self, controlador, segmentos):
        super().__init__()
        self.controlador = controlador
        self.segmentos = segmentos
        self.title("Editar segmentos")
        self.geometry("800x450")  # Aumentamos el ancho
        self.entries = []
        self._crear_widgets()
        self._precargar()

    def _crear_widgets(self):
        tk.Label(self, text=f"Segmentos existentes: {len(self.segmentos)}").pack(pady=5)

        # Contenedor horizontal para tabla + imagen
        contenedor = tk.Frame(self)
        contenedor.pack(pady=10, fill="both", expand=True)

        # Marco para tabla
        self.marco = tk.Frame(contenedor)
        self.marco.pack(side="left", padx=20, fill="x", expand=True)

        # Encabezados
        cols = ["Diámetro (m)", "Longitud (m)", "Coef. Hazzen"]
        for j, c in enumerate(cols):
            tk.Label(self.marco, text=c, borderwidth=1, relief="solid").grid(row=0, column=j, padx=2)

        # Filas
        for i in range(len(self.segmentos)):
            fila = []
            for j in range(len(cols)):
                e = tk.Entry(self.marco, width=12)
                e.grid(row=i + 1, column=j, padx=2, pady=2)
                fila.append(e)
            self.entries.append(fila)

        # Imagen decorativa a la derecha (ruta segura)
        try:
            imagen_path = ruta_recurso("recursos/imagen_segmentos.png")
            imagen = Image.open(imagen_path).resize((350, 300))
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            label_img = tk.Label(contenedor, image=self.imagen_tk)
            label_img.pack(side="right", padx=20, pady=10)
        except Exception as e:
            print("No se pudo cargar la imagen:", e)

        # Botón guardar
        tk.Button(self, text="Guardar cambios", command=self._aceptar).pack(pady=10)

    def _precargar(self):
        for i, seg in enumerate(self.segmentos):
            self.entries[i][0].insert(0, seg.diametro)
            self.entries[i][1].insert(0, seg.longitud)
            self.entries[i][2].insert(0, seg.coeficiente)

    def _aceptar(self):
        nueva = []
        try:
            for i, row in enumerate(self.entries):
                d = float(row[0].get())
                L = float(row[1].get())
                C = float(row[2].get())
                nueva.append(self.controlador.crear_segmento(i + 1, d, L, C))
        except:
            messagebox.showerror("Error", "Revise los datos de edición")
            return
        self.controlador.recibir_segmentos(nueva)
        self.destroy()
