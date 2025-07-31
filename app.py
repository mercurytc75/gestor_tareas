from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Tarea
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    completada = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_limite = db.Column(db.DateTime, nullable=True)
    prioridad = db.Column(db.String(20), default='media')  # baja, media, alta

# Crear las tablas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tareas = Tarea.query.order_by(Tarea.fecha_creacion.desc()).all()
    return render_template('index.html', tareas=tareas)

@app.route('/tarea/nueva', methods=['GET', 'POST'])
def nueva_tarea():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha_limite_str = request.form['fecha_limite']
        prioridad = request.form['prioridad']
        
        fecha_limite = None
        if fecha_limite_str:
            try:
                fecha_limite = datetime.strptime(fecha_limite_str, '%Y-%m-%d')
            except ValueError:
                flash('Formato de fecha inválido', 'error')
                return redirect(url_for('nueva_tarea'))
        
        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_limite=fecha_limite,
            prioridad=prioridad
        )
        
        db.session.add(nueva_tarea)
        db.session.commit()
        flash('Tarea creada exitosamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('nueva_tarea.html')

@app.route('/tarea/<int:id>/editar', methods=['GET', 'POST'])
def editar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    
    if request.method == 'POST':
        tarea.titulo = request.form['titulo']
        tarea.descripcion = request.form['descripcion']
        fecha_limite_str = request.form['fecha_limite']
        tarea.prioridad = request.form['prioridad']
        
        if fecha_limite_str:
            try:
                tarea.fecha_limite = datetime.strptime(fecha_limite_str, '%Y-%m-%d')
            except ValueError:
                flash('Formato de fecha inválido', 'error')
                return redirect(url_for('editar_tarea', id=id))
        else:
            tarea.fecha_limite = None
        
        db.session.commit()
        flash('Tarea actualizada exitosamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('editar_tarea.html', tarea=tarea)

@app.route('/tarea/<int:id>/eliminar', methods=['POST'])
def eliminar_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    flash('Tarea eliminada exitosamente!', 'success')
    return redirect(url_for('index'))

@app.route('/tarea/<int:id>/toggle', methods=['POST'])
def toggle_tarea(id):
    tarea = Tarea.query.get_or_404(id)
    tarea.completada = not tarea.completada
    db.session.commit()
    return jsonify({'completada': tarea.completada})

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