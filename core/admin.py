from django.contrib import admin
from .models import Cliente, Proyecto, Tarea, Pago, Soporte

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'email', 'telefono', 'creado']
    search_fields = ['nombre', 'empresa', 'email']

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cliente', 'estado', 'monto_total', 'creado']
    list_filter = ['estado', 'tipo']
    search_fields = ['nombre', 'cliente__nombre']

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'estado', 'prioridad']
    list_filter = ['estado', 'prioridad']

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'tipo', 'monto', 'pagado', 'fecha_esperada']
    list_filter = ['pagado', 'tipo']

@admin.register(Soporte)
class SoporteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'tipo', 'estado', 'prioridad']
    list_filter = ['estado', 'tipo', 'prioridad']
