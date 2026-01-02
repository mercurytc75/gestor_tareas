# 🚀 GUÍA RÁPIDA DE INICIO

## En 3 pasos, tu aplicación lista:

### 1️⃣ Instala dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecuta la aplicación
```bash
python run.py
```

### 3️⃣ Abre en el navegador
```
http://localhost:5000
```

---

## 🎮 Primeros pasos

### ✅ Crear una tarea
1. Haz clic en **"Nueva Tarea"**
2. Completa el título (obligatorio)
3. Agrupa descripción, fecha y prioridad (opcional)
4. Haz clic en **"Crear Tarea"**

### 📋 Ver tus tareas
- La página principal muestra todas tus tareas
- Verás estadísticas en los 4 cuadros de arriba
- Usa el checkbox para marcar como completada

### 🔍 Buscar y filtrar
- **Busca**: Escribe en "Buscar" para filtrar por título/descripción
- **Filtra**: Selecciona "Todas", "Pendientes" o "Completadas"
- **Ordena**: Por "Reciente", "Prioridad" o "Fecha límite"

### ✏️ Editar o eliminar
- Haz clic en el menú (⋮) en la tarjeta
- Selecciona "Editar" o "Eliminar"

---

## 🎨 Personalización

### Cambiar colores
Edita `static/css/style.css`, línea 1-10:
```css
:root {
    --primary: #0d6efd;      /* Color principal (azul) */
    --success: #198754;      /* Prioridad baja (verde) */
    --warning: #ffc107;      /* Prioridad media (amarillo) */
    --danger: #dc3545;       /* Prioridad alta (rojo) */
}
```

### Cambiar puerto
En `run.py`, línea 18:
```python
app.run(port=8000)  # Cambiar 5000 por tu puerto
```

### Cambiar tema
Modo oscuro requiere agregar CSS. Para ahora, usa DevTools:
```
F12 → Settings → Preferences → Dark mode ✓
```

---

## 🔐 Cambiar contraseña secreta

En `config.py`, línea 6:
```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu-nueva-clave-super-segura'
```

O mejor aún, crea un `.env`:
```bash
copy .env.example .env
# Edita .env y cambia SECRET_KEY
```

---

## 🧪 Probar la aplicación

### Crear datos de prueba
```bash
python -c "
from app import app
from models import db, Tarea
from datetime import datetime, timedelta

with app.app_context():
    # Limpiar tareas anteriores (opcional)
    Tarea.query.delete()
    
    # Crear tareas de prueba
    tareas = [
        Tarea(titulo='Aprender Flask', prioridad='alta', 
              fecha_limite=datetime.now() + timedelta(days=3)),
        Tarea(titulo='Mejorar UI', prioridad='media', descripcion='Agregar dark mode'),
        Tarea(titulo='Escribir tests', prioridad='baja', completada=False),
    ]
    
    for tarea in tareas:
        db.session.add(tarea)
    
    db.session.commit()
    print(f'✓ {len(tareas)} tareas de prueba creadas')
"
```

### Correr tests
```bash
pytest test_app.py -v
```

---

## 🐛 Problemas comunes

### Error: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"
```bash
# Puerto 5000 en uso, cambiar a otro:
# En run.py: app.run(port=8000)
python run.py
```

### Error: "database is locked"
```bash
# Cierra todas las ventanas de la app
# Elimina instance/tareas.db
# Ejecuta nuevamente
```

### Los estilos no cargan
```bash
# Limpia caché del navegador
Ctrl+Shift+Del (Chrome)
Ctrl+Shift+Supr (Firefox)
```

---

## 📁 Estructura de carpetas

```
tu-proyecto/
├── app.py                    ← Ejecutar: python app.py
├── run.py                    ← O ejecutar: python run.py
├── config.py                 ← Configuración
├── models.py                 ← Tareas (BD)
├── routes.py                 ← Rutas
├── validators.py             ← Validación
├── requirements.txt          ← pip install -r
├── static/
│   ├── css/style.css        ← Estilos (NO editar línea 1-20)
│   └── js/main.js           ← Interactividad
└── templates/
    ├── base.html            ← Base (NO editar)
    ├── index.html           ← Página principal
    ├── nueva_tarea.html     ← Crear
    └── editar_tarea.html    ← Editar
```

---

## 💡 Consejos

1. **Antes de cambiar código**:
   - Haz backup: `copy app.py app.py.bak`
   - Anota el cambio en un archivo

2. **Para agregar características**:
   - Modifica `models.py` (agregar campos)
   - Modifica `routes.py` (agregar rutas)
   - Modifica templates (agregar UI)

3. **Para mejorar visualmente**:
   - Todo está en `static/css/style.css`
   - Variables de color en línea 1-10
   - Clases Bootstrap reutilizables

4. **Para entender el código**:
   - Lee primero `app.py` (punto de entrada)
   - Luego `models.py` (estructura)
   - Luego `routes.py` (lógica)

---

## ✨ Próximos pasos (Opcional)

### Agregar usuarios
1. Instala Flask-Login: `pip install Flask-Login`
2. Modifica models.py para agregar Usuario
3. Crea rutas de login/registro

### Agregar notificaciones por email
1. Instala Flask-Mail: `pip install Flask-Mail`
2. Configura en config.py
3. Agrega función de email en routes.py

### Desplegar a la nube
1. Prepara para producción (cambiar DEBUG a False)
2. Usa Heroku, PythonAnywhere o similar
3. Configura variables de entorno en la plataforma

---

## 📞 Necesitas ayuda?

- Lee `README.md` para documentación completa
- Lee `CAMBIOS.md` para saber qué se mejoró
- Revisa `test_app.py` para ver ejemplos de uso
- Abre un issue en GitHub

---

**¡Listo! Ahora tienes una aplicación Flask profesional** 🎉

Disfruta desarrollando y personalizando tu Gestor de Tareas.
