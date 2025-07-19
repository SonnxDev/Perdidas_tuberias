from controlador.controlador import Controlador
from vista.ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    app = VentanaPrincipal()
    controlador = Controlador(app)
    app.controlador = controlador
    app.mainloop()