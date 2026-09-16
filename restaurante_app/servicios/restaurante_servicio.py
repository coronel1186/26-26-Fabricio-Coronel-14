from typing import List, Optional, Dict, Set
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        self._archivo_servicio: ArchivoServicio = archivo_servicio
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._productos_por_codigo: Dict[str, Producto] = {}
        self._usuarios_por_identificacion: Dict[str, Usuario] = {}

        self.cargar_datos()

    def cargar_datos(self) -> None:
        self._productos = self._archivo_servicio.cargar_productos()
        self._usuarios = self._archivo_servicio.cargar_usuarios()
        self._reconstruir_indices()

    def _reconstruir_indices(self) -> None:
        self._productos_por_codigo.clear()
        self._usuarios_por_identificacion.clear()

        for p in self._productos:
            self._productos_por_codigo[p.codigo] = p

        for u in self._usuarios:
            self._usuarios_por_identificacion[u.identificacion] = u

    def validar_acceso(self, identificacion_o_usuario: str, contrasena: str) -> Optional[Usuario]:
        if not identificacion_o_usuario or not contrasena:
            return None
        identificacion_o_usuario = identificacion_o_usuario.strip()
        contrasena = contrasena.strip()

        usuario = self.buscar_usuario(identificacion_o_usuario)
        if usuario is None:
            for u in self._usuarios:
                if u.nombre.lower() == identificacion_o_usuario.lower():
                    usuario = u
                    break

        if usuario and usuario.validar_clave(contrasena):
            return usuario
        return None

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        return self._productos_por_codigo.get(codigo.strip())

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        return self._usuarios_por_identificacion.get(identificacion.strip())

    def registrar_producto(self, producto: Producto) -> bool:
        if producto.codigo in self._productos_por_codigo:
            return False
        self._productos.append(producto)
        self._productos_por_codigo[producto.codigo] = producto
        self._archivo_servicio.guardar_productos(self._productos)
        return True

    def actualizar_producto(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        self._archivo_servicio.guardar_productos(self._productos)
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        if codigo in self._productos_por_codigo:
            del self._productos_por_codigo[codigo]
        self._archivo_servicio.guardar_productos(self._productos)
        return True

    def obtener_categorias(self) -> List[str]:
        categorias: Set[str] = {p.categoria for p in self._productos}
        categorias_base = {"Comida Rápida", "Pizzas", "Bebidas", "Ensaladas", "Postres"}
        return sorted(list(categorias.union(categorias_base)))

    def listar_productos(self) -> List[Producto]:
        return self._productos.copy()

    def listar_usuarios(self) -> List[Usuario]:
        return self._usuarios.copy()
    