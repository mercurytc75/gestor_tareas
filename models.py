"""
Modelos de base de datos
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class PriorityEnum(str, Enum):
    """Enumeración de prioridades"""
    BAJA = 'baja'
    MEDIA = 'media'
    ALTA = 'alta'

    @property
    def display_name(self):
        return self.value.capitalize()

    @property
    def badge_color(self):
        colors = {
            'baja': 'success',
            'media': 'warning',
            'alta': 'danger'
        }
        return colors.get(self.value, 'secondary')

class Tarea(db.Model):
    """Modelo de Tarea"""
    __tablename__ = 'tareas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=True)
    completada = db.Column(db.Boolean, default=False, index=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fecha_limite = db.Column(db.DateTime, nullable=True, index=True)
    prioridad = db.Column(db.String(20), default=PriorityEnum.MEDIA.value)
    
    def __repr__(self):
        return f'<Tarea {self.id}: {self.titulo}>'
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'completada': self.completada,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'fecha_limite': self.fecha_limite.isoformat() if self.fecha_limite else None,
            'prioridad': self.prioridad
        }
    
    @property
    def dias_restantes(self):
        """Calcular días restantes hasta la fecha límite"""
        if not self.fecha_limite:
            return None
        if self.completada:
            return None
        
        dias = (self.fecha_limite.date() - datetime.utcnow().date()).days
        return dias
    
    @property
    def esta_vencida(self):
        """Verificar si la tarea está vencida"""
        if not self.fecha_limite or self.completada:
            return False
        return datetime.utcnow() > self.fecha_limite
    
    @property
    def get_priority_enum(self):
        """Obtener el enum de prioridad"""
        try:
            return PriorityEnum(self.prioridad)
        except (ValueError, KeyError):
            return PriorityEnum.MEDIA
