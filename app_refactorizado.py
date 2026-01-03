"""
GESTOR DE TAREAS v2.0 - VERSIÓN REFACTORIZADA
Un único archivo principal que contiene toda la lógica
Estructura limpia y mantenible sin excesiva modularización
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from enum import Enum

# ==================== CONFIGURACIÓN ====================

class Config:
    """Configuración centralizada"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tareas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# ==================== INICIALIZACIÓN ====================

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# ==================== MODELOS ====================

class Tarea(db.Model):
    """Modelo de Tarea con propiedades útiles"""
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=True)
    completada = db.Column(db.Boolean, default=False, index=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fecha_limite = db.Column(db.DateTime, nullable=True, index=True)
    prioridad = db.Column(db.String(20), default='media')
    
    @property
    def dias_restantes(self):
        if not self.fecha_limite or self.completada:
            return None
        dias = (self.fecha_limite.date() - datetime.utcnow().date()).days
        return dias
    
    @property
    def esta_vencida(self):
        return self.fecha_limite and not self.completada and datetime.utcnow() > self.fecha_limite
    
    @property
    def color_prioridad(self):
        colores = {'baja': 'success', 'media': 'warning', 'alta': 'danger'}
        return colores.get(self.prioridad, 'secondary')

# ==================== VALIDADORES ====================

def validar_tarea(titulo, descripcion, fecha_limite_str, prioridad):
    """Valida datos de tarea y retorna (es_valido, errores, datos)"""
    errores = []
    
    titulo = (titulo or '').strip()
    if not titulo:
        errores.append('El título es obligatorio')
    elif len(titulo) > 100:
        errores.append('El título no puede exceder 100 caracteres')
    
    descripcion = (descripcion or '').strip()
    if len(descripcion) > 1000:
        errores.append('La descripción no puede exceder 1000 caracteres')
    
    if prioridad not in ['baja', 'media', 'alta']:
        errores.append('Prioridad inválida')
    
    fecha_limite = None
    if fecha_limite_str:
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, '%Y-%m-%d')
            if fecha_limite.date() < datetime.utcnow().date():
                errores.append('La fecha límite no puede ser en el pasado')
        except ValueError:
            errores.append('Formato de fecha inválido')
    
    return len(errores) == 0, errores, {
        'titulo': titulo,
        'descripcion': descripcion,
        'fecha_limite': fecha_limite,
        'prioridad': prioridad
    }

# ==================== RUTAS ====================

@app.route('/')
def index():
    """Página principal con filtros y búsqueda"""
    filtro = request.args.get('filtro', 'todas')
    orden = request.args.get('orden', 'reciente')
    buscar = request.args.get('buscar', '').strip()
    
    # Query base
    query = Tarea.query
    
    # Filtros
    if filtro == 'pendientes':
        query = query.filter_by(completada=False)
    elif filtro == 'completadas':
        query = query.filter_by(completada=True)
    
    # Búsqueda
    if buscar:
        query = query.filter(
            (Tarea.titulo.ilike(f'%{buscar}%')) |
            (Tarea.descripcion.ilike(f'%{buscar}%'))
        )
    
    # Ordenamiento
    if orden == 'prioridad':
        prioridad_orden = {'alta': 1, 'media': 2, 'baja': 3}
        tareas = query.all()
        tareas.sort(key=lambda t: (prioridad_orden.get(t.prioridad, 4), t.fecha_creacion.timestamp()), reverse=True)
    elif orden == 'fecha_limite':
        query = query.filter(Tarea.fecha_limite.isnot(None))
        tareas = query.order_by(Tarea.fecha_limite.asc()).all()
    else:
        tareas = query.order_by(Tarea.fecha_creacion.desc()).all()
    
    # Estadísticas
    total = Tarea.query.count()
    completadas = Tarea.query.filter_by(completada=True).count()
    pendientes = total - completadas
    
    return render_template(
        'index.html',
        tareas=tareas,
        filtro=filtro,
        orden=orden,
        buscar=buscar,
        total_tareas=total,
        tareas_completadas=completadas,
        tareas_pendientes=pendientes
    )

@app.route('/tarea/nueva', methods=['GET', 'POST'])
def nueva_tarea():
    """Crear nueva tarea"""
    if request.method == 'POST':
        es_valido, errores, datos = validar_tarea(
            request.form.get('titulo'),
            request.form.get('descripcion'),
            request.form.get('fecha_limite'),
            request.form.get('prioridad', 'media')
        )
        
        if not es_valido:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('nueva_tarea'))
        
        try:
            tarea = Tarea(**datos)
            db.session.add(tarea)
            db.session.commit()
            flash('¡Tarea creada exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la tarea', 'error')
            return redirect(url_for('nueva_tarea'))
    
    return render_template('nueva_tarea.html')

@app.route('/tarea/<int:id>/editar', methods=['GET', 'POST'])
def editar_tarea(id):
    """Editar tarea existente"""
    tarea = Tarea.query.get_or_404(id)
    
    if request.method == 'POST':
        es_valido, errores, datos = validar_tarea(
            request.form.get('titulo'),
            request.form.get('descripcion'),
            request.form.get('fecha_limite'),
            request.form.get('prioridad', 'media')
        )
        
        if not es_valido:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('editar_tarea', id=id))
        
        try:
            tarea.titulo = datos['titulo']
            tarea.descripcion = datos['descripcion']
            tarea.fecha_limite = datos['fecha_limite']
            tarea.prioridad = datos['prioridad']
            db.session.commit()
            flash('¡Tarea actualizada exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar la tarea', 'error')
            return redirect(url_for('editar_tarea', id=id))
    
    return render_template('editar_tarea.html', tarea=tarea)

@app.route('/tarea/<int:id>/eliminar', methods=['POST'])
def eliminar_tarea(id):
    """Eliminar tarea"""
    tarea = Tarea.query.get_or_404(id)
    try:
        db.session.delete(tarea)
        db.session.commit()
        flash('¡Tarea eliminada exitosamente!', 'success')
    except Exception:
        db.session.rollback()
        flash('Error al eliminar la tarea', 'error')
    return redirect(url_for('index'))

@app.route('/tarea/<int:id>/toggle', methods=['POST'])
def toggle_tarea(id):
    """Cambiar estado de completada (AJAX)"""
    tarea = Tarea.query.get_or_404(id)
    try:
        tarea.completada = not tarea.completada
        db.session.commit()
        return jsonify({'completada': tarea.completada, 'success': True})
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error al actualizar'}), 500

@app.route('/api/estadisticas')
def get_estadisticas():
    """API de estadísticas"""
    total = Tarea.query.count()
    completadas = Tarea.query.filter_by(completada=True).count()
    return jsonify({
        'total': total,
        'completadas': completadas,
        'pendientes': total - completadas
    })

@app.errorhandler(404)
def no_encontrado(e):
    """Manejo de errores 404"""
    return render_template('error.html', code=404, message='Página no encontrada'), 404

@app.errorhandler(500)
def error_servidor(e):
    """Manejo de errores 500"""
    db.session.rollback()
    return render_template('error.html', code=500, message='Error interno del servidor'), 500

# ==================== INICIALIZACIÓN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✓ Base de datos inicializada")
        print("✓ Ejecutando en http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
