import os
from flask import Flask
from config import config
from models import db
from routes import main_bp

def create_app(config_name=None):
    """Factory function para crear la aplicación"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    
    # Crear tablas de base de datos
    with app.app_context():
        db.create_all()
    
    return app

# Crear instancia de la aplicación
app = create_app()

@app.route('/tarea/<int:id>/completar', methods=['POST'])
def completar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    tarea.completada = True
    db.session.commit()
    flash('Tarea marcada como completada!', 'success')
    return redirect(url_for('index'))

@app.route('/tarea/<int:id>/descompletar', methods=['POST'])
def descompletar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    tarea.completada = False
    db.session.commit()
    flash('Tarea marcada como pendiente!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 