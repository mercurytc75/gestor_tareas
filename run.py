"""
Script para inicializar la aplicación
Ejecutar una vez: python run.py
"""
import os
from app import create_app, app, db
from models import Tarea

# Crear aplicación
if __name__ == '__main__':
    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()
        print("✓ Base de datos inicializada correctamente")
    
    # Ejecutar la aplicación
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.environ.get('FLASK_DEBUG', True)
    )
