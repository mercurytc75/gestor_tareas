# Gestor de Tareas

Una aplicación web moderna para gestionar tareas personales, construida con Flask y Bootstrap.

## Características

- ✅ **Interfaz moderna y responsiva** con Bootstrap 5
- ✅ **Gestión completa de tareas**: crear, editar, eliminar, marcar como completada
- ✅ **Sistema de prioridades**: baja, media, alta
- ✅ **Fechas límite** opcionales para cada tarea
- ✅ **Base de datos SQLite** para persistencia de datos
- ✅ **Interfaz intuitiva** con iconos y animaciones
- ✅ **Mensajes de confirmación** y notificaciones
- ✅ **Diseño responsive** que funciona en móviles y escritorio

## Instalación

1. **Clona o descarga el proyecto**
   ```bash
   git clone <url-del-repositorio>
   cd gestor_tareas
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación**
   ```bash
   python app.py
   ```

4. **Abre tu navegador**
   Ve a `http://localhost:5000`

## Uso

### Crear una nueva tarea
1. Haz clic en "Nueva Tarea" en la barra de navegación
2. Completa el formulario:
   - **Título** (obligatorio): nombre de la tarea
   - **Descripción** (opcional): detalles adicionales
   - **Fecha límite** (opcional): fecha de vencimiento
   - **Prioridad**: baja, media o alta
3. Haz clic en "Crear Tarea"

### Gestionar tareas existentes
- **Marcar como completada**: usa el checkbox en cada tarjeta de tarea
- **Editar**: haz clic en el menú de tres puntos y selecciona "Editar"
- **Eliminar**: haz clic en el menú de tres puntos y selecciona "Eliminar"

### Características visuales
- **Colores de prioridad**: verde (baja), amarillo (media), rojo (alta)
- **Tareas completadas**: aparecen con opacidad reducida y texto tachado
- **Animaciones**: las tarjetas se elevan al pasar el mouse
- **Notificaciones**: mensajes de confirmación que desaparecen automáticamente

## Estructura del proyecto

```
gestor_tareas/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal
│   ├── nueva_tarea.html  # Formulario de nueva tarea
│   └── editar_tarea.html # Formulario de edición
└── tareas.db             # Base de datos SQLite (se crea automáticamente)
```

## Tecnologías utilizadas

- **Backend**: Flask (Python)
- **Base de datos**: SQLite con SQLAlchemy
- **Frontend**: Bootstrap 5, Font Awesome
- **JavaScript**: Vanilla JS para interactividad

## Personalización

### Cambiar la clave secreta
En `app.py`, modifica la línea:
```python
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
```

### Cambiar la base de datos
Para usar otra base de datos, modifica en `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tu_base_de_datos.db'
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request


