"""
Arranque unificado con hilos: python run.py
"""
import os
import sys
import threading
from pathlib import Path

# Añadir 'src' al path para que las importaciones internas funcionen
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

# Ahora podemos importar los módulos que están dentro de src
from app import app, db
from info import mostrar_resumen

def run_flask():
    """Ejecuta el servidor Flask."""
    with app.app_context():
        db.create_all()
        print('Base de datos lista (tablas creadas si faltaban).')

    debug = os.environ.get('FLASK_DEBUG', '1').lower() not in ('0', 'false', 'no')
    # Usamos use_reloader=False para evitar problemas con hilos en desarrollo
    app.run(host='0.0.0.0', port=5000, debug=debug, use_reloader=False)

def run_info():
    """Ejecuta el script de información."""
    mostrar_resumen()

if __name__ == '__main__':
    # Crear hilos para ejecutar las tareas simultáneamente
    thread_flask = threading.Thread(target=run_flask)
    thread_info = threading.Thread(target=run_info)

    # Iniciar hilos
    thread_info.start()
    thread_flask.start()

    # Esperar a que terminen (aunque el de Flask es infinito hasta que se pare)
    thread_info.join()
    thread_flask.join()
