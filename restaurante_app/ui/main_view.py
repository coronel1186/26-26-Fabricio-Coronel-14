import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
from modelos.producto import Producto

class MainView(tk.Frame):
    def __init__(self, parent: tk.Widget, restaurante_servicio, usuario_actual, on_logout: Callable) -> None:
        super().__init__(parent)
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.on_logout = on_logout

        self._crear_componentes()

    def _crear_componentes(self) -> None:
        # Barra superior con datos de usuario y botón de salida
        top_bar = ttk.Frame(self, padding="10")
        top_bar.pack(fill="x", side="top")

        lbl_bienvenida = ttk.Label(
            top_bar, 
            text=f"Bienvenido/a, {self.usuario_actual.nombre} | Sistema de Gestión", 
            font=("Helvetica", 11, "bold")
        )
        lbl_bienvenida.pack(side="left")

        btn_logout = ttk.Button(
            top_bar, 
            text="Cerrar Sesión", 
            command=self.on_logout
        )
        btn_logout.pack(side="right")

        ttk.Separator(self, orient="horizontal").pack(fill="x")

        # Contenedor principal con pestañas (Notebook)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Pestaña 1: Gestión de Productos (Formulario + Botones + Tabla)
        tab_productos = ttk.Frame(notebook, padding="10")
        notebook.add(tab_productos, text="📦 Gestión de Productos")

        # Pestaña 2: Usuarios Registrados
        tab_usuarios = ttk.Frame(notebook, padding="10")
        notebook.add(tab_usuarios, text="👥 Usuarios Registrados")

        # Pestaña 3: Operaciones de Ventas
        tab_operaciones = ttk.Frame(notebook, padding="10")
        notebook.add(tab_operaciones, text="🛒 Operaciones (Ventas)")

        # Configurar las pestañas
        self._configurar_tab_productos(tab_productos)
        self._configurar_tab_usuarios(tab_usuarios)
        self._configurar_tab_operaciones(tab_operaciones)

    def _configurar_tab_productos(self, parent: ttk.Frame) -> None:
        # --- CONTENEDOR 1: FORMULARIO DE DATOS (LabelFrame + grid) ---
        frm_datos = ttk.LabelFrame(parent, text=" Formulario de Producto ", padding="12")
        frm_datos.pack(fill="x", side="top", pady=(0, 10))

        ttk.Label(frm_datos, text="Código:", font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.entry_codigo = ttk.Entry(frm_datos, width=15)
        self.entry_codigo.grid(row=0, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(frm_datos, text="Nombre del Plato:", font=("Helvetica", 9, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.entry_nombre = ttk.Entry(frm_datos, width=30)
        self.entry_nombre.grid(row=0, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(frm_datos, text="Categoría:", font=("Helvetica", 9, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.combo_categoria = ttk.Combobox(
            frm_datos, 
            values=self.restaurante_servicio.obtener_categorias(), 
            width=18, 
            state="normal"
        )
        self.combo_categoria.grid(row=1, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(frm_datos, text="Precio ($):", font=("Helvetica", 9, "bold")).grid(row=1, column=2, sticky="w", padx=5, pady=4)
        self.entry_precio = ttk.Entry(frm_datos, width=12)
        self.entry_precio.grid(row=1, column=3, sticky="w", padx=5, pady=4)

        ttk.Label(frm_datos, text="Stock Inicial:", font=("Helvetica", 9, "bold")).grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.entry_stock = ttk.Entry(frm_datos, width=15)
        self.entry_stock.grid(row=2, column=1, sticky="w", padx=5, pady=4)

        # --- CONTENEDOR 2: BOTONES DE ACCIÓN (Frame + pack) ---
        frm_acciones = ttk.Frame(parent, padding="5")
        frm_acciones.pack(fill="x", side="top", pady=(0, 10))

        btn_registrar = ttk.Button(frm_acciones, text="➕ Registrar Producto", command=self._registrar_producto)
        btn_registrar.pack(side="left", padx=5)

        btn_actualizar = ttk.Button(frm_acciones, text="✏️ Actualizar Producto", command=self._actualizar_producto)
        btn_actualizar.pack(side="left", padx=5)

        btn_eliminar = ttk.Button(frm_acciones, text="🗑️ Eliminar Producto", command=self._eliminar_producto)
        btn_eliminar.pack(side="left", padx=5)

        btn_limpiar = ttk.Button(frm_acciones, text="🧹 Limpiar Campos", command=self._limpiar_formulario)
        btn_limpiar.pack(side="right", padx=5)

        # --- CONTENEDOR 3: ÁREA DE VISUALIZACIÓN / TABLA (LabelFrame + Treeview + Scrollbar) ---
        frm_tabla = ttk.LabelFrame(parent, text=" Productos Registrados en el Menú ", padding="10")
        frm_tabla.pack(fill="both", expand=True, side="bottom")

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_productos = ttk.Treeview(frm_tabla, columns=columnas, show="headings", selectmode="browse")

        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Nombre Comercial")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.heading("precio", text="Precio Unitario ($)")
        self.tree_productos.heading("stock", text="Stock Disponible")

        self.tree_productos.column("codigo", width=80, anchor="center")
        self.tree_productos.column("nombre", width=220, anchor="w")
        self.tree_productos.column("categoria", width=140, anchor="center")
        self.tree_productos.column("precio", width=100, anchor="e")
        self.tree_productos.column("stock", width=110, anchor="center")

        scrollbar = ttk.Scrollbar(frm_tabla, orient="vertical", command=self.tree_productos.yview)
        self.tree_productos.configure(yscrollcommand=scrollbar.set)

        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Vincular selección para cargar datos en el formulario
        self.tree_productos.bind("<<TreeviewSelect>>", self._cargar_producto_seleccionado)

        self._refrescar_tabla_productos()

    def _refrescar_tabla_productos(self) -> None:
        for row in self.tree_productos.get_children():
            self.tree_productos.delete(row)
        productos = self.restaurante_servicio.listar_productos()
        for p in productos:
            self.tree_productos.insert("", "end", values=(p.codigo, p.nombre, p.categoria, f"{p.precio:.2f}", p.stock))

        self.combo_categoria["values"] = self.restaurante_servicio.obtener_categorias()

    def _cargar_producto_seleccionado(self, event: tk.Event) -> None:
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return
        item_data = self.tree_productos.item(seleccion, "values")
        if item_data:
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.insert(0, item_data)

            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, item_data[1])

            self.combo_categoria.set(item_data[2])

            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, item_data[3])

            self.entry_stock.delete(0, tk.END)
            self.entry_stock.insert(0, item_data[4])

    def _limpiar_formulario(self) -> None:
        self.entry_codigo.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.combo_categoria.set("")
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)

    def _registrar_producto(self) -> None:
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.combo_categoria.get().strip()
        precio_str = self.entry_precio.get().strip()
        stock_str = self.entry_stock.get().strip()

        if not codigo or not nombre or not categoria or not precio_str or not stock_str:
            messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos del formulario.")
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
            nuevo_producto = Producto(codigo, nombre, categoria, precio, stock)
        except ValueError as e:
            messagebox.showerror("Error de Formato", f"Datos numéricos inválidos: {e}")
            return

        if self.restaurante_servicio.registrar_producto(nuevo_producto):
            messagebox.showinfo("Registro Exitoso", f"El producto [{codigo}] '{nombre}' ha sido registrado correctamente.")
            self._refrescar_tabla_productos()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Código Duplicado", f"Ya existe un producto registrado con el código '{codigo}'.")

    def _actualizar_producto(self) -> None:
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.combo_categoria.get().strip()
        precio_str = self.entry_precio.get().strip()
        stock_str = self.entry_stock.get().strip()

        if not codigo or not nombre or not categoria or not precio_str or not stock_str:
            messagebox.showwarning("Campos Incompletos", "Seleccione un producto de la tabla o ingrese todos los campos.")
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error de Formato", "El precio debe ser decimal y el stock un número entero.")
            return

        if self.restaurante_servicio.actualizar_producto(codigo, nombre, categoria, precio, stock):
            messagebox.showinfo("Actualización Exitosa", f"El producto [{codigo}] ha sido actualizado correctamente.")
            self._refrescar_tabla_productos()
            self._limpiar_formulario()
        else:
            messagebox.showerror("No Encontrado", f"No se encontró ningún producto registrado con el código '{codigo}'.")

    def _eliminar_producto(self) -> None:
        codigo = self.entry_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Selección Requerida", "Por favor, seleccione un producto de la tabla para eliminar.")
            return

        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el producto [{codigo}]?")
        if confirmar:
            if self.restaurante_servicio.eliminar_producto(codigo):
                messagebox.showinfo("Eliminación Exitosa", f"El producto [{codigo}] fue eliminado correctamente.")
                self._refrescar_tabla_productos()
                self._limpiar_formulario()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar: el código [{codigo}] no existe.")

    def _configurar_tab_usuarios(self, parent: ttk.Frame) -> None:
        lbl = ttk.Label(parent, text="Usuarios Registrados para Acceso al Sistema", font=("Helvetica", 11, "bold"))
        lbl.pack(anchor="w", pady=(0, 10))

        columnas = ("identificacion", "nombre", "correo")
        tree = ttk.Treeview(parent, columns=columnas, show="headings", height=8)

        tree.heading("identificacion", text="ID / Usuario")
        tree.heading("nombre", text="Nombre Completo")
        tree.heading("correo", text="Correo Electrónico")

        tree.column("identificacion", width=100, anchor="center")
        tree.column("nombre", width=220, anchor="w")
        tree.column("correo", width=220, anchor="w")

        tree.pack(fill="both", expand=True, pady=(0, 10))

        usuarios = self.restaurante_servicio.listar_usuarios()
        for u in usuarios:
            tree.insert("", "end", values=(u.identificacion, u.nombre, u.correo))

    def _configurar_tab_operaciones(self, parent: ttk.Frame) -> None:
        lbl = ttk.Label(parent, text="Módulo de Ventas y Transacciones", font=("Helvetica", 11, "bold"))
        lbl.pack(anchor="w", pady=(0, 15))

        lbl_info = ttk.Label(
            parent,
            text="En esta Semana 14 se ha consolidado la gestión completa de Productos mediante componentes y contenedores.\n"
                 "El módulo gráfico de Ventas e Historial Transaccional se incorporará en los siguientes contenidos de la unidad.",
            font=("Helvetica", 10),
            justify="left"
        )
        lbl_info.pack(anchor="w", pady=(0, 20))

        btn_venta = ttk.Button(
            parent, 
            text="🛒 Realizar Venta de Producto", 
            command=self._mostrar_funcionalidad_pendiente
        )
        btn_venta.pack(anchor="w", pady=5, ipadx=10, ipady=3)

        btn_historial = ttk.Button(
            parent, 
            text="📋 Consultar Historial de Ventas", 
            command=self._mostrar_funcionalidad_pendiente
        )
        btn_historial.pack(anchor="w", pady=5, ipadx=10, ipady=3)

    def _mostrar_funcionalidad_pendiente(self) -> None:
        messagebox.showinfo(
            "Próximamente",
            "Funcionalidad que será incorporada posteriormente en los siguientes contenidos de la unidad."
        )
        