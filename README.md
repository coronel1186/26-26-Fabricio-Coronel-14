# Restaurante App - Componentes y Contenedores (Semana 14)

Este proyecto corresponde a la evolución del sistema **`restaurante_app`** para la **Semana 14** de la asignatura **Programación Orientada a Objetos**. En esta etapa se mejora la capa de presentación (`ui/`) mediante el uso estructurado de componentes, contenedores y gestores de geometría de **Tkinter/ttk**, conservando la arquitectura modular, la persistencia en archivos JSON y la separación de responsabilidades.

---

## 📌 Propósito de la Semana 14

1. **Separación de Capas:** La interfaz gráfica no le maneja ni modifica archivos JSON directamente; solicita todas las operaciones a `RestauranteServicio`.
2. **Jerarquía Visual y Contenedores:** Se organiza la ventana principal mediante áreas de trabajo independientes (`Notebook`, `LabelFrame`, `Frame`).
3. **Gestión de Productos:** Permite realizar operaciones de registro, consulta/carga, actualización y eliminación sobre los productos del menú.
4. **Persistencia Sincronizada:** Cada cambio desde la interfaz actualiza los datos en RAM, los mapas hash \\(\mathcal{O}(1)\\) y el archivo `productos.json`.

---

## 📂 Estructura del Repositorio

```text
restaurante_app/
├── datos/
│   ├── productos.json            # Persistencia física de productos e inventario
│   └── usuarios.json             # Persistencia física de usuarios y credenciales
├── modelos/
│   ├── __init__.py               # Paquete de modelos
│   ├── producto.py               # Entidad Producto
│   └── usuario.py                # Entidad Usuario
├── servicios/
│   ├── __init__.py               # Paquete de servicios
│   ├── archivo_servicio.py       # Lectura/Escritura JSON con control de excepciones
│   └── restaurante_servicio.py   # Lógica de negocio, CRUD e índices O(1)
├── ui/
│   ├── __init__.py               # Paquete de interfaz gráfica
│   ├── login_view.py             # Vista de acceso simulado (Login)
│   └── main_view.py              # Panel principal (Formulario + Botones + Tabla)
├── main.py                       # Orquestador Tkinter (Ventana única y mainloop)
└── README.md                     # Documentación técnica del proyecto


Componentes y Contenedores Utilizados
ttk.Notebook: Organiza las secciones en tres pestañas: Gestión de Productos, Usuarios Registrados y Operaciones.
ttk.LabelFrame: Agrupa y titula el Formulario de Producto y el Área de Tabla.
ttk.Entry / ttk.Combobox: Capturan entradas cortas de texto y opciones desplegables de categoría.
ttk.Button con command=: Ejecutan las acciones de Registrar, Actualizar, Eliminar y Limpiar Campos.
ttk.Treeview y ttk.Scrollbar: Muestran la lista formateada de productos. La selección de una fila (<<TreeviewSelect>>) carga automáticamente los datos en el formulario.

Gestores de Geometría Aplicados
grid(): Organiza etiquetas y entradas en el formulario en filas y columnas correlativas.
pack(): Distribuye los botones de acción en barras horizontales (side="left") y ajusta las pestañas principales.
🔑 Credenciales de Prueba
Usuario 1: U001 | Contraseña: 1234 (Carlos Gómez)
Usuario 2: U002 | Contraseña: admin (Ana López)
🚀 Pasos para Ejecutar
Sitúese en la raíz del proyecto:
cd restaurante_app
Ejecute la aplicación gráfica:
python main.py


