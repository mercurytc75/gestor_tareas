"""
Gestor de Tareas — fábrica de aplicación Flask.
"""
import os
from flask import Flask, render_template

from config import config as config_map
from models import db
from routes import main_bp


def create_app(config_name=None):
    """Crea y configura la aplicación."""
    name = config_name or os.environ.get('FLASK_ENV', 'development')
    if name not in config_map:
        name = 'default'

    app = Flask(__name__, instance_relative_config=True)
    
    # Asegurar que el root_path sea el directorio de este archivo
    app.root_path = os.path.dirname(__file__)
    app.config.from_object(config_map[name])

    os.makedirs(app.instance_path, exist_ok=True)
    # En testing la URI en memoria ya viene de TestingConfig; no sobrescribir.
    if not os.environ.get('DATABASE_URL') and name != 'testing':
        db_path = os.path.join(app.instance_path, 'tareas.db').replace('\\', '/')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    db.init_app(app)
    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def no_encontrado(_e):
        return render_template('error.html', code=404, message='Página no encontrada'), 404

    @app.errorhandler(500)
    def error_servidor(_e):
        db.session.rollback()
        return render_template('error.html', code=500, message='Error interno del servidor'), 500

    return app


app = create_app()

if __name__ == '__main__':
    # Si se ejecuta directamente desde src/, las importaciones funcionan
    with app.app_context():
        db.create_all()
    app.run(debug=True)
