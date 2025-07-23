from controlador.controlador import Controlador
from vista.ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    app = VentanaPrincipal(None)             # Primero creas la ventana sin controlador
    controlador = Controlador(app)           # Luego el controlador conoce la ventana
    app.controlador = controlador            # Se enlazan mutuamente
    app._crear_botones()                     # Ahora puedes crear los botones con el controlador activo
    app.mainloop()
