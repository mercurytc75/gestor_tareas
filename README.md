# Gestor de Tareas Profesional

Una aplicación web moderna y escalable para gestionar tareas personales, construida con **Flask**, **SQLAlchemy** y **Bootstrap 5**.

## 🌟 Características principales

✨ **Interfaz moderna y responsiva** con Bootstrap 5 y CSS personalizado
✅ **Gestión completa de tareas**: crear, editar, eliminar, marcar como completada
⚡ **Sistema de prioridades**: baja, media, alta con indicadores visuales
📅 **Fechas límite** con cálculo automático de días restantes
💾 **Base de datos SQLite** con modelos optimizados
🔍 **Búsqueda y filtros avanzados** para encontrar tareas rápidamente
📊 **Estadísticas en tiempo real** del progreso
🎯 **Validación robusta** en servidor y cliente
🎨 **Diseño escalable y mantenible** con arquitectura profesional
🚀 **API AJAX** para operaciones sin recargar la página
📱 **Totalmente responsive** en móviles, tablets y escritorio

## 🏗️ Arquitectura del Proyecto

```
gestor_tareas/
├── app.py                      # Aplicación principal con factory pattern
├── config.py                   # Configuración (desarrollo/producción/testing)
├── models.py                   # Modelos de base de datos
├── routes.py                   # Rutas y vistas
├── validators.py               # Validadores personalizados
├── run.py                      # Script para ejecutar la aplicación
├── test_app.py                 # Tests unitarios
├── requirements.txt            # Dependencias
├── .env.example                # Variables de entorno de ejemplo
├── instance/                   # Instancia de la app (base de datos)
├── static/
│   ├── css/
│   │   └── style.css          # Estilos profesionales y responsivos
│   └── js/
│       └── main.js            # JavaScript con funcionalidades avanzadas
└── templates/
    ├── base.html              # Template base con navbar y footer
    ├── index.html             # Página principal con estadísticas y filtros
    ├── nueva_tarea.html       # Formulario para crear tareas
    └── editar_tarea.html      # Formulario para editar tareas
```

## 📦 Instalación

### Requisitos
- Python 3.8+
- pip

### Pasos

1. **Clona o descarga el proyecto**
   ```bash
   git clone <tu-repositorio>
   cd gestor_tareas
   ```

2. **Crea un entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copia el archivo de variables de entorno**
   ```bash
   copy .env.example .env    # Windows
   cp .env.example .env      # Linux/Mac
   ```

5. **Ejecuta la aplicación**
   ```bash
   python run.py
   ```

6. **Abre tu navegador**
   ```
   http://localhost:5000
   ```

## 🎮 Uso

### Crear una nueva tarea
1. Haz clic en **"Nueva Tarea"** en la barra de navegación
2. Completa el formulario:
   - **Título** *(obligatorio)*: nombre de la tarea
   - **Descripción** *(opcional)*: detalles adicionales
   - **Fecha límite** *(opcional)*: fecha de vencimiento
   - **Prioridad**: 🟢 Baja, 🟡 Media o 🔴 Alta
3. Haz clic en **"Crear Tarea"**

### Gestionar tareas
- **Marcar como completada**: usa el checkbox en cada tarjeta
- **Editar**: haz clic en el menú (⋮) → "Editar"
- **Eliminar**: haz clic en el menú (⋮) → "Eliminar"

### Filtros y búsqueda
- **Buscar**: escribe en el campo de búsqueda para filtrar por título o descripción
- **Filtrar**: selecciona entre todas, pendientes o completadas
- **Ordenar**: ordena por fecha (reciente), prioridad o fecha límite

### Estadísticas
La página principal muestra:
- Total de tareas
- Tareas completadas
- Tareas pendientes
- Porcentaje de progreso

## 🎨 Características de Diseño

### Colores por Prioridad
- 🟢 **Baja**: Verde (#28a745)
- 🟡 **Media**: Amarillo (#ffc107)
- 🔴 **Alta**: Rojo (#dc3545)

### Elementos Interactivos
- Tarjetas con efecto hover (elevación y sombra)
- Checkboxes con validación en tiempo real
- Formularios con validación en cliente y servidor
- Notificaciones toast que desaparecen automáticamente
- Búsqueda instantánea

## 🔒 Seguridad

- ✅ Validación de entrada en servidor y cliente
- ✅ Protección CSRF mediante Flask
- ✅ Consultas paramétrizadas contra inyección SQL
- ✅ Variables de entorno para datos sensibles
- ✅ Manejo de errores sin exponer información sensible

## 💾 Tecnologías Utilizadas

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Backend** | Flask | 3.1.1 |
| **ORM** | SQLAlchemy | 2.0.42 |
| **Base de Datos** | SQLite | 3.x |
| **Frontend** | Bootstrap | 5.3.0 |
| **Iconos** | Font Awesome | 6.5.1 |
| **JavaScript** | Vanilla JS | ES6+ |

## 🌐 Compatibilidad

- ✅ Chrome/Edge (últimas versiones)
- ✅ Firefox (últimas versiones)
- ✅ Safari (últimas versiones)
- ✅ Responsive: Escritorio, Tablet, Móvil
- ✅ Sin dependencias externas locales (CDN para Bootstrap y FontAwesome)

## 🚀 Mejoras Implementadas

### Refactorización de Código
- Separación en módulos (`config.py`, `models.py`, `routes.py`, `validators.py`)
- Factory pattern para crear aplicación
- Modelos con métodos útiles
- Validadores reutilizables

### Mejoras de UI/UX
- Estadísticas en tiempo real
- Filtros y búsqueda avanzada
- Indicadores de días restantes
- Detección de tareas vencidas
- Animaciones suaves
- Notificaciones tipo toast
- Formularios mejorados con validación

### Funcionalidades Nuevas
- API AJAX para cambio de estado sin recargar
- Cálculo automático de días restantes
- Búsqueda por título y descripción
- Ordenamiento por prioridad
- Paginación (preparada)
- Estadísticas de progreso

## 📝 Configuración

### Variables de Entorno (.env)
```bash
FLASK_ENV=development          # development, production, testing
FLASK_DEBUG=1                  # Activar modo debug
SECRET_KEY=tu-clave-aqui       # Clave secreta para sesiones
DATABASE_URL=sqlite:///tareas.db
```

### Configuración por Entorno
- **Desarrollo**: Debug activado, validaciones permisivas
- **Producción**: Debug desactivado, validaciones estrictas
- **Testing**: Base de datos en memoria

## 📊 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Lista de tareas con filtros |
| GET | `/tarea/nueva` | Formulario nueva tarea |
| POST | `/tarea/nueva` | Crear tarea |
| GET | `/tarea/<id>/editar` | Formulario editar tarea |
| POST | `/tarea/<id>/editar` | Actualizar tarea |
| POST | `/tarea/<id>/eliminar` | Eliminar tarea |
| POST | `/tarea/<id>/toggle` | Cambiar estado (AJAX) |
| GET | `/api/estadisticas` | Obtener estadísticas (JSON) |

## 🧪 Testing

Ejecuta los tests unitarios:
```bash
pytest test_app.py -v
```

## 🌱 Mejoras Futuras

- [ ] Autenticación y usuarios múltiples
- [ ] Tareas recurrentes
- [ ] Recordatorios por email
- [ ] Exportar tareas a PDF
- [ ] Integración con Google Calendar
- [ ] Dark mode
- [ ] Aplicación PWA
- [ ] API REST pública

## 🐛 Solución de Problemas

### La aplicación no inicia
```bash
# Verifica Python
python --version

# Reinstala dependencias
pip install --upgrade -r requirements.txt

# Elimina base de datos antigua (cuidado con datos)
rm instance/tareas.db
python run.py
```

### Los estilos no cargan
- Limpia caché: `Ctrl+Shift+Supr` (Chrome) o `Ctrl+F5`
- Verifica que `static/css/style.css` existe
- Revisa la consola del navegador (F12)

### Las tareas no se guardan
- Verifica permisos de escritura en el directorio
- Comprueba espacio disponible en disco
- Revisa los logs en la consola

## 📄 Licencia

Este proyecto es de código abierto bajo licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/Mejora`)
3. Commit cambios (`git commit -m 'Agrega mejora'`)
4. Push (`git push origin feature/Mejora`)
5. Abre un Pull Request

## 📞 Soporte

¿Tienes preguntas? Abre un issue en el repositorio.

---

**Desarrollado con ❤️ usando Flask y Bootstrap | Versión 2.0 Mejorada**


