import os
import sys
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

class AplicacionRestaurante:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Restaurante App - Interfaz Gráfica (Semana 14)")
        self.root.geometry("720x580")
        self.root.minsize(640, 480)

        # Ruta base para la carpeta de datos JSON
        ruta_base = Path(__file__).resolve().parent
        carpeta_datos = ruta_base / "datos"

        # Inicialización de servicios
        self.archivo_servicio = ArchivoServicio(str(carpeta_datos))
        self.restaurante_servicio = RestauranteServicio(self.archivo_servicio)

        self.vista_actual = None
        self.usuario_autenticado = None

        self._configurar_estilos()
        self.mostrar_login()

    def _configurar_estilos(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

    def cambiar_vista(self, nueva_vista: tk.Frame) -> None:
        if self.vista_actual is not None:
            self.vista_actual.destroy()
        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self) -> None:
        self.usuario_autenticado = None
        login_view = LoginView(
            parent=self.root,
            restaurante_servicio=self.restaurante_servicio,
            on_login_success=self.on_login_exitoso
        )
        self.cambiar_vista(login_view)

    def on_login_exitoso(self, usuario: Usuario) -> None:
        self.usuario_autenticado = usuario
        self.mostrar_main_view()

    def mostrar_main_view(self) -> None:
        main_view = MainView(
            parent=self.root,
            restaurante_servicio=self.restaurante_servicio,
            usuario_actual=self.usuario_autenticado,
            on_logout=self.mostrar_login
        )
        self.cambiar_vista(main_view)

    def iniciar(self) -> None:
        self.root.mainloop()

def main() -> None:
    app = AplicacionRestaurante()
    app.iniciar()

if __name__ == "__main__":
    main()
    