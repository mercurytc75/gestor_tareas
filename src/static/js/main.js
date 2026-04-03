/**
 * Gestor de Tareas - Script Principal
 */

document.addEventListener('DOMContentLoaded', function() {

    // ==================== Toggle Tareas ====================
    const toggleTasks = document.querySelectorAll('.toggle-task');
    
    toggleTasks.forEach(checkbox => {
        checkbox.addEventListener('change', handleToggleTask);
    });

    function handleToggleTask(event) {
        const checkbox = event.currentTarget;
        const taskId = checkbox.dataset.taskId;
        const card = document.querySelector(`.task-card[data-task-id="${taskId}"]`)
            || document.querySelector(`[data-task-id="${taskId}"]`)?.closest('.task-card');
        if (!card) return;
        
        // Deshabilitar checkbox mientras se envía la solicitud
        checkbox.disabled = true;
        const originalChecked = checkbox.checked;
        
        // Agregar efecto de carga
        card.classList.add('loading');
        
        fetch(`/tarea/${taskId}/toggle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Error en la respuesta');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const label = checkbox.parentElement.querySelector('.form-check-label');
                
                if (data.completada) {
                    card.classList.add('completed');
                    label.innerHTML = '<span class="text-success"><i class="fas fa-check me-1"></i>Completada</span>';
                    showNotification('¡Tarea marcada como completada!', 'success');
                } else {
                    card.classList.remove('completed');
                    label.innerHTML = '<span class="text-muted">Marcar como completada</span>';
                    showNotification('Tarea marcada como pendiente', 'info');
                }
                
                // Actualizar estadísticas
                updateStatistics();
            } else {
                throw new Error(data.error || 'Error desconocido');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Revertir cambio
            checkbox.checked = !originalChecked;
            showNotification('Error al actualizar la tarea', 'error');
        })
        .finally(() => {
            checkbox.disabled = false;
            card.classList.remove('loading');
        });
    }

    // ==================== Mostrar Notificaciones ====================
    function showNotification(message, type = 'info') {
        const alertHtml = `
            <div class="toast alert alert-${type} alert-dismissible fade show" 
                 role="alert" data-bs-autohide="true" data-bs-delay="5000">
                <div class="d-flex align-items-center">
                    <i class="fas fa-${getIconByType(type)} me-2"></i>
                    <div class="flex-grow-1">${message}</div>
                </div>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const container = document.querySelector('.toast-container') || createToastContainer();
        const alertElement = document.createElement('div');
        alertElement.innerHTML = alertHtml;
        container.appendChild(alertElement.firstElementChild);
        
        const toast = new bootstrap.Toast(container.lastElementChild);
        toast.show();
        
        // Eliminar elemento después de que desaparezca
        setTimeout(() => {
            container.lastElementChild.remove();
        }, 6000);
    }

    function getIconByType(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '11';
        document.body.appendChild(container);
        return container;
    }

    // ==================== Actualizar Estadísticas ====================
    function updateStatistics() {
        fetch('/api/estadisticas')
            .then(response => response.json())
            .then(data => {
                const total = data.total ?? 0;
                const completadas = data.completadas ?? 0;
                const pendientes = data.pendientes ?? 0;
                const pct = total === 0 ? 0 : Math.round((completadas / total) * 100);
                const map = {
                    total: String(total),
                    completadas: String(completadas),
                    pendientes: String(pendientes),
                    porcentaje: pct + '%'
                };
                Object.keys(map).forEach(function(key) {
                    const el = document.querySelector('[data-stat="' + key + '"]');
                    if (el) el.textContent = map[key];
                });
            })
            .catch(function(err) { console.error('Error al actualizar estadísticas:', err); });
    }

    // ==================== Validación de Formularios ====================
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            // Validaciones personalizadas
            const titleInput = form.querySelector('#titulo');
            if (titleInput && !titleInput.value.trim()) {
                e.preventDefault();
                showNotification('El título es obligatorio', 'error');
                titleInput.focus();
            }
        });
    });

    // ==================== Autocompletado de Altura en Textarea ====================
    const textareas = document.querySelectorAll('textarea.form-control');
    
    textareas.forEach(textarea => {
        // Establecer altura inicial
        setTextareaHeight(textarea);
        
        // Escuchar cambios
        textarea.addEventListener('input', function() {
            setTextareaHeight(this);
        });
    });

    function setTextareaHeight(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 300) + 'px';
    }

    // ==================== Confirmación de Eliminación ====================
    const deleteButtons = document.querySelectorAll('button[onclick*="confirm"]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('onclick');
            if (message.includes('confirm')) {
                if (!confirm('¿Estás seguro de que quieres eliminar esta tarea?')) {
                    e.preventDefault();
                }
            }
        });
    });

    // ==================== Búsqueda en Tiempo Real (Opcional) ====================
    const searchInput = document.querySelector('#buscar');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            // Aquí puedes implementar búsqueda en tiempo real si lo deseas
        });
    }

    // ==================== Teclas de Atajo ====================
    document.addEventListener('keydown', function(e) {
        // Alt + N: Nueva Tarea
        if (e.altKey && e.key === 'n') {
            window.location.href = document.querySelector('a[href*="/tarea/nueva"]')?.href || '/tarea/nueva';
        }
        
        // Alt + H: Inicio
        if (e.altKey && e.key === 'h') {
            window.location.href = '/';
        }
    });

    // ==================== Detectar Cambios No Guardados ====================
    let formChanged = false;
    const editForms = document.querySelectorAll('form');
    
    editForms.forEach(form => {
        form.addEventListener('input', function() {
            formChanged = true;
        });
        
        form.addEventListener('submit', function() {
            formChanged = false;
        });
    });

    window.addEventListener('beforeunload', function(e) {
        if (formChanged) {
            e.preventDefault();
            e.returnValue = 'Tienes cambios sin guardar';
        }
    });

    // ==================== Utilidades ====================
    
    // Función para formatear fechas
    window.formatDate = function(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('es-ES', options);
    };

    // Función para verificar si hay conexión
    window.isOnline = function() {
        return navigator.onLine;
    };

    // Escuchar cambios de conectividad
    window.addEventListener('online', function() {
        showNotification('Conexión restaurada', 'success');
    });

    window.addEventListener('offline', function() {
        showNotification('Conexión perdida', 'warning');
    });

});

// Prevenir múltiples envíos de formulario
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (submitButton && !form.dataset.submitted) {
        form.dataset.submitted = true;
        submitButton.disabled = true;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
    }
}, true);
