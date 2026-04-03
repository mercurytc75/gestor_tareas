"""
Rutas de la aplicación
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from models import Tarea, db
from validators import validar_formulario_tarea

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """Página principal con listado de tareas"""
    # Parámetros de filtrado
    filtro = request.args.get('filtro', 'todas')  # todas, pendientes, completadas
    orden = request.args.get('orden', 'reciente')  # reciente, prioridad, fecha_limite
    buscar = request.args.get('buscar', '').strip()
    
    # Query base
    query = Tarea.query
    
    # Aplicar filtros
    if filtro == 'pendientes':
        query = query.filter_by(completada=False)
    elif filtro == 'completadas':
        query = query.filter_by(completada=True)
    
    # Aplicar búsqueda
    if buscar:
        query = query.filter(
            (Tarea.titulo.ilike(f'%{buscar}%')) |
            (Tarea.descripcion.ilike(f'%{buscar}%'))
        )
    
    # Aplicar ordenamiento
    if orden == 'prioridad':
        # Orden de prioridad: alta > media > baja
        prioridad_orden = {
            'alta': 1,
            'media': 2,
            'baja': 3
        }
        tareas = query.all()
        tareas.sort(key=lambda t: (prioridad_orden.get(t.prioridad, 4), t.fecha_creacion.timestamp()), reverse=True)
    elif orden == 'fecha_limite':
        query = query.filter(Tarea.fecha_limite.isnot(None))
        tareas = query.order_by(Tarea.fecha_limite.asc()).all()
    else:  # reciente
        tareas = query.order_by(Tarea.fecha_creacion.desc()).all()
    
    # Calcular estadísticas
    total_tareas = Tarea.query.count()
    tareas_completadas = Tarea.query.filter_by(completada=True).count()
    tareas_pendientes = total_tareas - tareas_completadas
    
    return render_template(
        'index.html',
        tareas=tareas,
        filtro=filtro,
        orden=orden,
        buscar=buscar,
        total_tareas=total_tareas,
        tareas_completadas=tareas_completadas,
        tareas_pendientes=tareas_pendientes
    )

@main_bp.route('/tarea/nueva', methods=['GET', 'POST'])
def nueva_tarea():
    """Crear nueva tarea"""
    if request.method == 'POST':
        es_valido, errores, datos = validar_formulario_tarea(request.form)
        
        if not es_valido:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('main.nueva_tarea'))
        
        try:
            tarea = Tarea(
                titulo=datos['titulo'],
                descripcion=datos['descripcion'],
                fecha_limite=datos['fecha_limite'],
                prioridad=datos['prioridad']
            )
            db.session.add(tarea)
            db.session.commit()
            flash('¡Tarea creada exitosamente!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la tarea', 'error')
            return redirect(url_for('main.nueva_tarea'))
    
    return render_template('nueva_tarea.html')

@main_bp.route('/tarea/<int:id>/editar', methods=['GET', 'POST'])
def editar_tarea(id):
    """Editar tarea existente"""
    tarea = Tarea.query.get_or_404(id)
    
    if request.method == 'POST':
        es_valido, errores, datos = validar_formulario_tarea(request.form)
        
        if not es_valido:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('main.editar_tarea', id=id))
        
        try:
            tarea.titulo = datos['titulo']
            tarea.descripcion = datos['descripcion']
            tarea.fecha_limite = datos['fecha_limite']
            tarea.prioridad = datos['prioridad']
            
            db.session.commit()
            flash('¡Tarea actualizada exitosamente!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar la tarea', 'error')
            return redirect(url_for('main.editar_tarea', id=id))
    
    return render_template('editar_tarea.html', tarea=tarea)

@main_bp.route('/tarea/<int:id>/eliminar', methods=['POST'])
def eliminar_tarea(id):
    """Eliminar tarea"""
    tarea = Tarea.query.get_or_404(id)
    
    try:
        db.session.delete(tarea)
        db.session.commit()
        flash('¡Tarea eliminada exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la tarea', 'error')
    
    return redirect(url_for('main.index'))

@main_bp.route('/tarea/<int:id>/toggle', methods=['POST'])
def toggle_tarea(id):
    """Cambiar estado de completada (AJAX)"""
    tarea = Tarea.query.get_or_404(id)
    
    try:
        tarea.completada = not tarea.completada
        db.session.commit()
        return jsonify({
            'completada': tarea.completada,
            'success': True
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error al actualizar la tarea'
        }), 500

@main_bp.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    """Obtener estadísticas (API)"""
    total = Tarea.query.count()
    completadas = Tarea.query.filter_by(completada=True).count()
    pendientes = total - completadas
    
    por_prioridad = {}
    for prioridad in ['baja', 'media', 'alta']:
        por_prioridad[prioridad] = Tarea.query.filter_by(prioridad=prioridad, completada=False).count()
    
    return jsonify({
        'total': total,
        'completadas': completadas,
        'pendientes': pendientes,
        'por_prioridad': por_prioridad
    })
