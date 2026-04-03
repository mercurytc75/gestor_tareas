"""
Arranque en desarrollo: python run.py
"""
import os
from app import app, db
from models import Tarea  # noqa: F401 — registra el modelo en SQLAlchemy

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Base de datos lista (tablas creadas si faltaban).')

    debug = os.environ.get('FLASK_DEBUG', '1').lower() not in ('0', 'false', 'no')
    app.run(host='0.0.0.0', port=5000, debug=debug)
