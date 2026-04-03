"""
Tests para la aplicación de tareas
Ejecutar: python -m pytest
"""
import sys
from pathlib import Path

# Añadir 'src' al path para que las importaciones internas funcionen
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

import pytest
from app import create_app
from models import db, Tarea
from datetime import datetime, timedelta


@pytest.fixture
def app():
    """Crear aplicación de pruebas"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de pruebas"""
    return app.test_client()


def test_index_vacio(client):
    """Probar página principal sin tareas"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'No hay tareas a\xc3\xban' in response.data


def test_crear_tarea(client):
    """Probar creación de tarea"""
    response = client.post('/tarea/nueva', data={
        'titulo': 'Test Tarea',
        'descripcion': 'Descripción de test',
        'fecha_limite': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'prioridad': 'alta'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test Tarea' in response.data


def test_editar_tarea(client, app):
    """Probar edición de tarea"""
    with app.app_context():
        tarea = Tarea(
            titulo='Tarea Original',
            descripcion='Descripción original',
            prioridad='media'
        )
        db.session.add(tarea)
        db.session.commit()
        tarea_id = tarea.id
    
    response = client.post(f'/tarea/{tarea_id}/editar', data={
        'titulo': 'Tarea Editada',
        'descripcion': 'Descripción editada',
        'prioridad': 'alta'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Tarea Editada' in response.data


def test_eliminar_tarea(client, app):
    """Probar eliminación de tarea"""
    with app.app_context():
        tarea = Tarea(titulo='Tarea a eliminar', prioridad='media')
        db.session.add(tarea)
        db.session.commit()
        tarea_id = tarea.id
    
    response = client.post(f'/tarea/{tarea_id}/eliminar', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        tarea = Tarea.query.get(tarea_id)
        assert tarea is None


def test_toggle_tarea(client, app):
    """Probar cambio de estado de tarea"""
    with app.app_context():
        tarea = Tarea(titulo='Test', prioridad='media', completada=False)
        db.session.add(tarea)
        db.session.commit()
        tarea_id = tarea.id
    
    response = client.post(f'/tarea/{tarea_id}/toggle')
    assert response.status_code == 200
    
    with app.app_context():
        tarea = Tarea.query.get(tarea_id)
        assert tarea.completada is True
