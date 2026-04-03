"""
Validadores para formularios
"""
from datetime import datetime


def validar_formulario_tarea(form_data):
    """
    Validar los datos del formulario de tarea
    Retorna: (es_valido, errores)
    """
    errores = []
    
    titulo = form_data.get('titulo', '').strip()
    if not titulo:
        errores.append('El título es obligatorio')
    elif len(titulo) > 100:
        errores.append('El título no puede exceder 100 caracteres')
    
    descripcion = form_data.get('descripcion', '').strip()
    if len(descripcion) > 1000:
        errores.append('La descripción no puede exceder 1000 caracteres')
    
    prioridad = form_data.get('prioridad', 'media')
    prioridades_validas = ['baja', 'media', 'alta']
    if prioridad not in prioridades_validas:
        errores.append('Prioridad inválida')
    
    fecha_limite_str = form_data.get('fecha_limite', '')
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
