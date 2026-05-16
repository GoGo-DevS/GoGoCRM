from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Clientes
    path('clientes/', views.clientes_list, name='clientes'),
    path('clientes/nuevo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),

    # Proyectos
    path('proyectos/', views.proyectos_list, name='proyectos'),
    path('proyectos/nuevo/', views.proyecto_create, name='proyecto_create'),
    path('proyectos/<int:pk>/', views.proyecto_detail, name='proyecto_detail'),
    path('proyectos/<int:pk>/editar/', views.proyecto_edit, name='proyecto_edit'),
    path('proyectos/<int:pk>/kanban/', views.proyecto_kanban, name='proyecto_kanban'),

    # Tareas (AJAX)
    path('tareas/nueva/', views.tarea_create, name='tarea_create'),
    path('tareas/<int:pk>/estado/', views.tarea_estado, name='tarea_estado'),
    path('tareas/<int:pk>/eliminar/', views.tarea_delete, name='tarea_delete'),

    # Pagos
    path('pagos/', views.pagos_list, name='pagos'),
    path('proyectos/<int:pk>/pago/nuevo/', views.pago_create, name='pago_create'),
    path('pagos/<int:pk>/toggle/', views.pago_toggle, name='pago_toggle'),

    # Soporte
    path('soporte/', views.soporte_list, name='soporte'),
    path('proyectos/<int:pk>/soporte/nuevo/', views.soporte_create, name='soporte_create'),
    path('soporte/<int:pk>/estado/', views.soporte_estado, name='soporte_estado'),
]
